"""
Empire Builder - Main Flask Application
A comprehensive web-based empire building strategy game
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import time
import threading
from dataclasses import asdict
from datetime import timedelta

# Import our models and game logic
from models import GameDatabase, Empire, BattleSystem, UNIT_COSTS, UNIT_STATS
from ai_system import ai_manager, create_ai_empires, initialize_ai_system
from auth import auth_db, login_required, get_current_user, login_user, logout_user

# Try to import alliance system, but don't fail if it's not available
try:
    from alliance_system import alliance_db, Alliance, AllianceRole
    ALLIANCE_SYSTEM_AVAILABLE = True
    print("✅ Alliance system loaded successfully")
except ImportError as e:
    print(f"⚠️ Alliance system not available: {e}")
    ALLIANCE_SYSTEM_AVAILABLE = False
    alliance_db = None
    Alliance = None
    AllianceRole = None

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'empire-builder-secret-key-2024')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

socketio = SocketIO(app, cors_allowed_origins="*")

# Global game state
db = GameDatabase()
active_battles = {}  # battle_id -> battle_data

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json or request.content_type == 'application/json':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            remember_me = data.get('remember_me', False)
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me') == 'on'
        
        if not username or not password:
            if request.is_json:
                return jsonify({'error': 'Username and password are required'}), 400
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        user = auth_db.authenticate_user(username, password)
        if user:
            login_user(user, remember_me)
            
            if request.is_json:
                redirect_url = url_for('dashboard') if user.empire_id else url_for('create_empire')
                return jsonify({'success': True, 'redirect': redirect_url})
            
            return redirect(url_for('dashboard') if user.empire_id else url_for('create_empire'))
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid username or password'}), 401
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json or request.content_type == 'application/json':
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
        else:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            error = 'All fields are required'
            if request.is_json:
                return jsonify({'error': error}), 400
            flash(error, 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            error = 'Passwords do not match'
            if request.is_json:
                return jsonify({'error': error}), 400
            flash(error, 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            error = 'Password must be at least 6 characters long'
            if request.is_json:
                return jsonify({'error': error}), 400
            flash(error, 'error')
            return render_template('register.html')
        
        # Create user
        try:
            user_id = auth_db.create_user(username, email, password)
            
            if user_id:
                if request.is_json:
                    return jsonify({'success': True, 'message': 'Account created successfully'})
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                error = 'Username or email already exists'
                if request.is_json:
                    return jsonify({'error': error}), 400
                flash(error, 'error')
        except Exception as e:
            error = f'Registration failed: {str(e)}'
            if request.is_json:
                return jsonify({'error': error}), 500
            flash(error, 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_empire', methods=['GET', 'POST'])
@login_required
def create_empire():
    current_user = get_current_user()
    
    # Check if user already has an empire
    if current_user.empire_id:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.json
        empire_id = db.create_empire(
            data['name'], 
            data['ruler'], 
            data['lat'], 
            data['lng']
        )
        
        # Link the empire to the user
        auth_db.link_user_to_empire(current_user.id, empire_id)
        session['empire_id'] = empire_id
        
        # Create AI opponents if this is the first human player
        all_empires = db.get_all_empires()
        human_empires = [e for e in all_empires if not e.is_ai]
        
        if len(human_empires) <= 1:  # First human player
            ai_empire_ids = create_ai_empires(db, count=3)
            for ai_id in ai_empire_ids:
                ai_manager.add_ai_player(ai_id, difficulty="normal")
        
        return jsonify({'success': True, 'empire_id': empire_id})
    
    return render_template('create_empire.html')

@app.route('/dashboard')
@login_required
def dashboard():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empire = db.get_empire(current_user.empire_id)
    if not empire:
        return redirect(url_for('create_empire'))
    
    return render_template('dashboard.html', empire=asdict(empire), user=current_user)

@app.route('/world_map')
@login_required
def world_map():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empires = db.get_all_empires()
    return render_template('world_map.html', empires=[asdict(e) for e in empires])

@app.route('/military')
@login_required
def military():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empire = db.get_empire(current_user.empire_id)
    return render_template('military.html', empire=asdict(empire), unit_costs=UNIT_COSTS, unit_stats=UNIT_STATS)

@app.route('/cities')
@login_required
def cities():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empire = db.get_empire(current_user.empire_id)
    from models import BUILDING_TYPES, CITY_COSTS, CITY_STATS, LAND_COST_PER_ACRE
    
    return render_template('cities.html', 
                         empire=asdict(empire), 
                         building_types=BUILDING_TYPES,
                         city_costs=CITY_COSTS,
                         city_stats=CITY_STATS,
                         land_cost=LAND_COST_PER_ACRE)

# Alliance Routes (only if alliance system is available)
if ALLIANCE_SYSTEM_AVAILABLE:
    @app.route('/alliances')
    @login_required
    def alliances():
        current_user = get_current_user()
        
        if not current_user.empire_id:
            return redirect(url_for('create_empire'))
        
        # Get user's alliance if they have one
        user_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
        user_role = None
        
        if user_alliance:
            # Get user's role in the alliance
            members = alliance_db.get_alliance_members(user_alliance.id)
            for member in members:
                if member['empire_id'] == current_user.empire_id:
                    user_role = member['role']
                    break
        
        # Get all alliances with leader names
        all_alliances = alliance_db.get_all_alliances()
        for alliance in all_alliances:
            leader_empire = db.get_empire(alliance.leader_id)
            alliance.leader_name = leader_empire.name if leader_empire else "Unknown"
        
        # Get pending invites for the user
        pending_invites = alliance_db.get_empire_invites(current_user.empire_id)
        
        return render_template('alliances.html', 
                             alliances=all_alliances,
                             user_alliance=user_alliance,
                             user_role=user_role,
                             pending_invites=pending_invites)

    @app.route('/alliance/<alliance_id>')
    @login_required
    def alliance_details(alliance_id):
        current_user = get_current_user()
        
        if not current_user.empire_id:
            return redirect(url_for('create_empire'))
        
        alliance = alliance_db.get_alliance(alliance_id)
        if not alliance:
            flash('Alliance not found', 'error')
            return redirect(url_for('alliances'))
        
        # Get alliance members
        members = alliance_db.get_alliance_members(alliance_id)
        
        # Check if user is a member and get their role
        is_member = False
        user_role = None
        user_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
        
        if user_alliance and user_alliance.id == alliance_id:
            is_member = True
            for member in members:
                if member['empire_id'] == current_user.empire_id:
                    user_role = member['role']
                    break
        
        # Get current empire for contribution limits
        empire = db.get_empire(current_user.empire_id)
        
        return render_template('alliance_details.html',
                             alliance=alliance,
                             members=members,
                             is_member=is_member,
                             user_role=user_role,
                             user_alliance=user_alliance,
                             empire=asdict(empire))

@app.route('/api/empire/<empire_id>')
def get_empire_api(empire_id):
    empire = db.get_empire(empire_id)
    if empire:
        return jsonify(asdict(empire))
    return jsonify({'error': 'Empire not found'}), 404

@app.route('/api/train_units', methods=['POST'])
@login_required
def train_units():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    total_cost = {'gold': 0, 'iron': 0, 'oil': 0, 'food': 0}
    
    # Calculate total cost
    for unit_type, count in data.items():
        if unit_type in UNIT_COSTS and count > 0:
            for resource, cost in UNIT_COSTS[unit_type].items():
                total_cost[resource] += cost * count
    
    # Check if empire can afford it
    for resource, cost in total_cost.items():
        if empire.resources.get(resource, 0) < cost:
            return jsonify({'error': f'Not enough {resource}'}), 400
    
    # Deduct resources and add units
    for resource, cost in total_cost.items():
        empire.resources[resource] -= cost
    
    for unit_type, count in data.items():
        if unit_type in UNIT_COSTS and count > 0:
            empire.military[unit_type] = empire.military.get(unit_type, 0) + count
    
    db.update_empire(empire)
    
    return jsonify({'success': True, 'empire': asdict(empire)})

@app.route('/api/attack', methods=['POST'])
@login_required
def attack_empire():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    data = request.json
    attacker = db.get_empire(current_user.empire_id)
    defender = db.get_empire(data['target_id'])
    attacking_units = data['units']
    
    if not defender:
        return jsonify({'error': 'Target empire not found'}), 404
    
    # Validate attacking units
    for unit_type, count in attacking_units.items():
        if count > attacker.military.get(unit_type, 0):
            return jsonify({'error': f'Not enough {unit_type}'}), 400
    
    # Calculate battle
    battle_result = BattleSystem.calculate_battle(attacker, defender, attacking_units)
    
    # Update empires
    db.update_empire(attacker)
    db.update_empire(defender)
    
    # Emit real-time battle updates
    socketio.emit('battle_result', battle_result, room=f'empire_{attacker.id}')
    socketio.emit('battle_result', battle_result, room=f'empire_{defender.id}')
    
    return jsonify(battle_result)

@app.route('/api/build_city', methods=['POST'])
@login_required
def build_city():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    city_name = data.get('name', '')
    city_type = data.get('type', 'small')
    
    if not city_name:
        return jsonify({'error': 'City name required'}), 400
    
    if db.build_city(empire, city_name, city_type):
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Cannot build city - insufficient resources'}), 400

@app.route('/api/build_building', methods=['POST'])
@login_required
def build_building():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    city_id = data.get('city_id', '')
    building_type = data.get('building_type', '')
    
    if not city_id or not building_type:
        return jsonify({'error': 'City ID and building type required'}), 400
    
    if db.build_building(empire, city_id, building_type):
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Cannot build - check requirements'}), 400

@app.route('/api/buy_land', methods=['POST'])
@login_required
def buy_land():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    acres = data.get('acres', 0)
    
    if acres <= 0:
        return jsonify({'error': 'Invalid land amount'}), 400
    
    if db.buy_land(empire, acres):
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Insufficient gold'}), 400

    # Alliance API Routes
    @app.route('/api/create_alliance', methods=['POST'])
    @login_required
    def create_alliance_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    # Check if user is already in an alliance
    existing_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
    if existing_alliance:
        return jsonify({'error': 'You are already in an alliance'}), 400
    
    data = request.json
    name = data.get('name', '').strip()
    tag = data.get('tag', '').strip().upper()
    description = data.get('description', '').strip()
    color = data.get('color', '#007bff')
    
    if not name or not tag:
        return jsonify({'error': 'Alliance name and tag are required'}), 400
    
    if len(tag) < 3 or len(tag) > 5:
        return jsonify({'error': 'Alliance tag must be 3-5 characters'}), 400
    
    alliance_id = alliance_db.create_alliance(name, tag, description, current_user.empire_id, color)
    
    if alliance_id:
        return jsonify({'success': True, 'alliance_id': alliance_id})
    else:
        return jsonify({'error': 'Alliance name or tag already exists'}), 400

@app.route('/api/invite_to_alliance', methods=['POST'])
@login_required
def invite_to_alliance_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    # Check if user has permission to invite
    user_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
    if not user_alliance:
        return jsonify({'error': 'You are not in an alliance'}), 400
    
    members = alliance_db.get_alliance_members(user_alliance.id)
    user_role = None
    for member in members:
        if member['empire_id'] == current_user.empire_id:
            user_role = member['role']
            break
    
    if user_role not in ['leader', 'officer']:
        return jsonify({'error': 'Only leaders and officers can invite members'}), 403
    
    data = request.json
    empire_name = data.get('empire_name', '').strip()
    message = data.get('message', '').strip()
    
    if not empire_name:
        return jsonify({'error': 'Empire name is required'}), 400
    
    # Find the empire by name
    target_empire = None
    all_empires = db.get_all_empires()
    for empire in all_empires:
        if empire.name.lower() == empire_name.lower():
            target_empire = empire
            break
    
    if not target_empire:
        return jsonify({'error': 'Empire not found'}), 404
    
    invite_id = alliance_db.invite_to_alliance(user_alliance.id, target_empire.id, 
                                              current_user.empire_id, message)
    
    if invite_id:
        return jsonify({'success': True, 'invite_id': invite_id})
    else:
        return jsonify({'error': 'Failed to send invitation (empire may already be in an alliance or invitation already exists)'}), 400

@app.route('/api/respond_alliance_invite', methods=['POST'])
@login_required
def respond_alliance_invite_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    data = request.json
    invite_id = data.get('invite_id')
    accept = data.get('accept', False)
    
    if not invite_id:
        return jsonify({'error': 'Invite ID is required'}), 400
    
    success = alliance_db.respond_to_invite(invite_id, accept)
    
    if success:
        action = 'accepted' if accept else 'declined'
        return jsonify({'success': True, 'message': f'Invitation {action} successfully'})
    else:
        return jsonify({'error': 'Failed to respond to invitation (may be expired or invalid)'}), 400

@app.route('/api/leave_alliance', methods=['POST'])
@login_required
def leave_alliance_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    success = alliance_db.leave_alliance(current_user.empire_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Left alliance successfully'})
    else:
        return jsonify({'error': 'Failed to leave alliance (leaders must transfer leadership first)'}), 400

@app.route('/api/kick_alliance_member', methods=['POST'])
@login_required
def kick_alliance_member_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    user_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
    if not user_alliance:
        return jsonify({'error': 'You are not in an alliance'}), 400
    
    data = request.json
    target_empire_id = data.get('empire_id')
    
    if not target_empire_id:
        return jsonify({'error': 'Empire ID is required'}), 400
    
    success = alliance_db.kick_member(user_alliance.id, target_empire_id, current_user.empire_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Member kicked successfully'})
    else:
        return jsonify({'error': 'Failed to kick member (insufficient permissions)'}), 403

@app.route('/api/promote_alliance_member', methods=['POST'])
@login_required
def promote_alliance_member_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    user_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
    if not user_alliance:
        return jsonify({'error': 'You are not in an alliance'}), 400
    
    data = request.json
    target_empire_id = data.get('empire_id')
    new_role = data.get('new_role')
    
    if not target_empire_id or not new_role:
        return jsonify({'error': 'Empire ID and new role are required'}), 400
    
    try:
        role_enum = AllianceRole(new_role)
    except ValueError:
        return jsonify({'error': 'Invalid role'}), 400
    
    success = alliance_db.promote_member(user_alliance.id, target_empire_id, 
                                        current_user.empire_id, role_enum)
    
    if success:
        return jsonify({'success': True, 'message': 'Member role updated successfully'})
    else:
        return jsonify({'error': 'Failed to update member role (insufficient permissions)'}), 403

@app.route('/api/contribute_to_alliance', methods=['POST'])
@login_required
def contribute_to_alliance_api():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    user_alliance = alliance_db.get_empire_alliance(current_user.empire_id)
    if not user_alliance:
        return jsonify({'error': 'You are not in an alliance'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    if not empire:
        return jsonify({'error': 'Empire not found'}), 400
    
    data = request.json
    gold = data.get('gold', 0)
    food = data.get('food', 0)
    iron = data.get('iron', 0)
    oil = data.get('oil', 0)
    
    # Validate contribution amounts
    if gold < 0 or food < 0 or iron < 0 or oil < 0:
        return jsonify({'error': 'Contribution amounts cannot be negative'}), 400
    
    if gold > empire.gold or food > empire.food or iron > empire.iron or oil > empire.oil:
        return jsonify({'error': 'Insufficient resources'}), 400
    
    if gold == 0 and food == 0 and iron == 0 and oil == 0:
        return jsonify({'error': 'Must contribute at least one resource'}), 400
    
    # Deduct resources from empire
    empire.gold -= gold
    empire.food -= food
    empire.iron -= iron
    empire.oil -= oil
    
    # Update empire in database
    db.update_empire(empire)
    
    # Add to alliance treasury
    success = alliance_db.contribute_to_treasury(user_alliance.id, current_user.empire_id, 
                                                gold, food, iron, oil)
    
    if success:
        return jsonify({'success': True, 'message': 'Resources contributed successfully'})
    else:
        # Rollback empire resources if alliance contribution failed
        empire.gold += gold
        empire.food += food
        empire.iron += iron
        empire.oil += oil
        db.update_empire(empire)
        return jsonify({'error': 'Failed to contribute resources'}), 500

# Error handlers for JSON requests
@app.errorhandler(500)
def handle_internal_error(error):
    if request.is_json or request.content_type == 'application/json':
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('error.html', error='Internal server error'), 500

@app.errorhandler(404)
def handle_not_found(error):
    if request.is_json or request.content_type == 'application/json':
        return jsonify({'error': 'Not found'}), 404
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(400)
def handle_bad_request(error):
    if request.is_json or request.content_type == 'application/json':
        return jsonify({'error': 'Bad request'}), 400
    return render_template('error.html', error='Bad request'), 400

# Socket.IO events for real-time features
@socketio.on('connect')
def on_connect():
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        join_room(f'empire_{current_user.empire_id}')
        emit('connected', {'status': 'Connected to Empire Builder', 'username': current_user.username})

@socketio.on('disconnect')
def on_disconnect():
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        leave_room(f'empire_{current_user.empire_id}')

@socketio.on('join_empire')
def on_join_empire(data):
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        join_room(f'empire_{current_user.empire_id}')

# Background tasks for AI and resource generation
def background_tasks():
    """Background thread for AI actions and resource generation"""
    while True:
        try:
            # Generate resources for all empires
            empires = db.get_all_empires()
            for empire in empires:
                # Base resource generation based on land and population
                generation_rate = empire.land / 1000
                empire.resources['gold'] += int(10 * generation_rate)
                empire.resources['food'] += int(15 * generation_rate)
                empire.resources['iron'] += int(5 * generation_rate)
                empire.resources['oil'] += int(3 * generation_rate)
                
                # Building production bonus
                building_production = db.calculate_building_production(empire)
                for resource, amount in building_production.items():
                    empire.resources[resource] += amount
                
                # Population growth
                growth_rate = 0.01
                empire.resources['population'] += int(empire.resources['population'] * growth_rate)
                
                db.update_empire(empire)
            
            time.sleep(60)  # Run every minute
            
        except Exception as e:
            print(f"Background task error: {e}")
            time.sleep(60)

# Start background thread
background_thread = threading.Thread(target=background_tasks, daemon=True)
background_thread.start()

# Initialize AI system
initialize_ai_system()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Empire Builder on port {port}")
    print(f"🔧 Debug mode: {debug}")
    
    # Always use allow_unsafe_werkzeug=True for deployment compatibility
    socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)