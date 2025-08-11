"""
Empire Builder - Production Flask Application (without alliance system)
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
                return jsonify({'success': True, 'message': 'Login successful'})
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            if request.is_json:
                return jsonify({'error': error}), 401
            flash(error, 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json or request.content_type == 'application/json':
            data = request.get_json()
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
        else:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        error = None
        if not username or not email or not password:
            error = 'All fields are required'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters'
        elif password != confirm_password:
            error = 'Passwords do not match'
        elif '@' not in email or '.' not in email:
            error = 'Please enter a valid email address'
        
        if error:
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
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

# Main game routes
@app.route('/')
def index():
    current_user = get_current_user()
    if current_user:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empire = db.get_empire(current_user.empire_id)
    if not empire:
        return redirect(url_for('create_empire'))
    
    # Get all empires for the map
    all_empires = db.get_all_empires()
    
    return render_template('dashboard.html', 
                         empire=asdict(empire), 
                         all_empires=[asdict(e) for e in all_empires],
                         unit_costs=UNIT_COSTS,
                         unit_stats=UNIT_STATS)

@app.route('/create_empire', methods=['GET', 'POST'])
@login_required
def create_empire():
    current_user = get_current_user()
    
    # Check if user already has an empire
    if current_user.empire_id:
        existing_empire = db.get_empire(current_user.empire_id)
        if existing_empire:
            return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        ruler = request.form.get('ruler', '').strip()
        location_x = float(request.form.get('location_x', 0))
        location_y = float(request.form.get('location_y', 0))
        
        if not name or not ruler:
            flash('Empire name and ruler name are required', 'error')
            return render_template('create_empire.html')
        
        # Create the empire
        empire = Empire(
            name=name,
            ruler=ruler,
            location_x=location_x,
            location_y=location_y
        )
        
        empire_id = db.create_empire(empire)
        if empire_id:
            # Link the empire to the user
            auth_db.link_user_to_empire(current_user.id, empire_id)
            flash(f'Empire "{name}" created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Empire name already exists. Please choose a different name.', 'error')
    
    return render_template('create_empire.html')

@app.route('/military')
@login_required
def military():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empire = db.get_empire(current_user.empire_id)
    all_empires = db.get_all_empires()
    
    return render_template('military.html', 
                         empire=asdict(empire), 
                         all_empires=[asdict(e) for e in all_empires],
                         unit_costs=UNIT_COSTS,
                         unit_stats=UNIT_STATS)

@app.route('/cities')
@login_required
def cities():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    empire = db.get_empire(current_user.empire_id)
    
    # City costs and stats
    CITY_COSTS = {
        'small': 5000,
        'medium': 15000,
        'large': 40000
    }
    
    CITY_STATS = {
        'small': {'max_buildings': 15, 'defense_bonus': 0.1, 'production_bonus': 0.0},
        'medium': {'max_buildings': 35, 'defense_bonus': 0.2, 'production_bonus': 0.1},
        'large': {'max_buildings': 60, 'defense_bonus': 0.3, 'production_bonus': 0.2}
    }
    
    LAND_COST_PER_ACRE = 100
    
    return render_template('cities.html', 
                         empire=asdict(empire),
                         city_costs=CITY_COSTS,
                         city_stats=CITY_STATS,
                         land_cost=LAND_COST_PER_ACRE)

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
    
    # Check if empire has enough resources
    if (empire.gold >= total_cost['gold'] and 
        empire.iron >= total_cost['iron'] and 
        empire.oil >= total_cost['oil'] and 
        empire.food >= total_cost['food']):
        
        # Deduct resources
        empire.gold -= total_cost['gold']
        empire.iron -= total_cost['iron']
        empire.oil -= total_cost['oil']
        empire.food -= total_cost['food']
        
        # Add units
        for unit_type, count in data.items():
            if unit_type in UNIT_COSTS and count > 0:
                if unit_type == 'infantry':
                    empire.infantry += count
                elif unit_type == 'tanks':
                    empire.tanks += count
                elif unit_type == 'aircraft':
                    empire.aircraft += count
                elif unit_type == 'ships':
                    empire.ships += count
        
        # Update military power
        empire.update_military_power()
        
        # Save to database
        db.update_empire(empire)
        
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Insufficient resources'}), 400

@app.route('/api/attack', methods=['POST'])
@login_required
def attack():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    attacker = db.get_empire(current_user.empire_id)
    data = request.json
    
    defender_id = data.get('defender_id')
    attacking_units = data.get('units', {})
    
    if not defender_id:
        return jsonify({'error': 'Defender ID required'}), 400
    
    defender = db.get_empire(defender_id)
    if not defender:
        return jsonify({'error': 'Defender not found'}), 404
    
    if attacker.id == defender.id:
        return jsonify({'error': 'Cannot attack yourself'}), 400
    
    # Validate attacking units
    total_attacking = sum(attacking_units.values())
    if total_attacking == 0:
        return jsonify({'error': 'Must send at least one unit'}), 400
    
    # Check if attacker has enough units
    if (attacking_units.get('infantry', 0) > attacker.infantry or
        attacking_units.get('tanks', 0) > attacker.tanks or
        attacking_units.get('aircraft', 0) > attacker.aircraft or
        attacking_units.get('ships', 0) > attacker.ships):
        return jsonify({'error': 'Insufficient units'}), 400
    
    # Create battle system and execute battle
    battle_system = BattleSystem()
    result = battle_system.execute_battle(attacker, defender, attacking_units)
    
    # Update empires in database
    db.update_empire(attacker)
    db.update_empire(defender)
    
    return jsonify(result)

@app.route('/api/build_city', methods=['POST'])
@login_required
def build_city():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    city_type = data.get('city_type')
    city_name = data.get('city_name', '').strip()
    
    if not city_type or not city_name:
        return jsonify({'error': 'City type and name are required'}), 400
    
    if db.build_city(empire, city_type, city_name):
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Failed to build city (insufficient resources or land)'}), 400

@app.route('/api/build_building', methods=['POST'])
@login_required
def build_building():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    city_id = data.get('city_id')
    building_type = data.get('building_type')
    
    if not city_id or not building_type:
        return jsonify({'error': 'City ID and building type are required'}), 400
    
    if db.build_building(empire, city_id, building_type):
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Failed to build building (insufficient resources or space)'}), 400

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
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def on_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('join_empire')
def on_join_empire(data):
    empire_id = data.get('empire_id')
    if empire_id:
        join_room(f'empire_{empire_id}')
        print(f'Client {request.sid} joined empire room: {empire_id}')

@socketio.on('leave_empire')
def on_leave_empire(data):
    empire_id = data.get('empire_id')
    if empire_id:
        leave_room(f'empire_{empire_id}')
        print(f'Client {request.sid} left empire room: {empire_id}')

def resource_generation_loop():
    """Background thread for resource generation"""
    while True:
        try:
            empires = db.get_all_empires()
            for empire in empires:
                old_resources = {
                    'gold': empire.gold,
                    'food': empire.food,
                    'iron': empire.iron,
                    'oil': empire.oil,
                    'population': empire.population
                }
                
                # Generate resources
                db.generate_resources(empire)
                
                # Check if resources changed significantly
                resource_changed = (
                    abs(empire.gold - old_resources['gold']) > 10 or
                    abs(empire.food - old_resources['food']) > 10 or
                    abs(empire.iron - old_resources['iron']) > 5 or
                    abs(empire.oil - old_resources['oil']) > 5 or
                    abs(empire.population - old_resources['population']) > 5
                )
                
                if resource_changed:
                    # Emit update to empire room
                    socketio.emit('empire_update', asdict(empire), room=f'empire_{empire.id}')
            
            # AI actions
            ai_manager.process_ai_actions(db)
            
        except Exception as e:
            print(f"Error in resource generation: {e}")
        
        time.sleep(60)  # Run every minute

# Initialize AI system and start background threads
def initialize_game():
    """Initialize the game systems"""
    print("🎮 Initializing Empire Builder...")
    
    # Create AI empires if none exist
    all_empires = db.get_all_empires()
    ai_empires = [e for e in all_empires if e.is_ai]
    
    if len(ai_empires) < 3:
        print("🤖 Creating AI empires...")
        create_ai_empires(db, target_count=5)
    
    # Initialize AI system
    initialize_ai_system(db)
    
    # Start background resource generation
    resource_thread = threading.Thread(target=resource_generation_loop, daemon=True)
    resource_thread.start()
    
    print("✅ Empire Builder initialized successfully!")

if __name__ == '__main__':
    initialize_game()
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Empire Builder on port {port}")
    print(f"🔧 Debug mode: {os.environ.get('FLASK_ENV') == 'development'}")
    
    socketio.run(app, 
                host='0.0.0.0', 
                port=port, 
                debug=os.environ.get('FLASK_ENV') == 'development',
                allow_unsafe_werkzeug=True)