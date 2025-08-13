"""
Empire Builder - Supabase Enhanced Flask Application
Real-time multiplayer empire building with Supabase PostgreSQL
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import time
import threading
from dataclasses import asdict
from datetime import timedelta

# Import Supabase enhanced models
from models_supabase import (
    supabase_db, supabase_battle_system, initialize_supabase_models,
    UNIT_COSTS, UNIT_STATS, BUILDING_TYPES, Empire
)
from ai_system import ai_manager, create_ai_empires, initialize_ai_system
from auth import auth_db, login_required, get_current_user, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'empire-builder-supabase-key-2024')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

socketio = SocketIO(app, cors_allowed_origins="*")

# Global game state with Supabase
db = supabase_db
battle_system = supabase_battle_system
active_battles = {}

# Initialize Supabase on startup
@app.before_first_request
def initialize_supabase():
    """Initialize Supabase system"""
    try:
        using_supabase = initialize_supabase_models()
        if using_supabase:
            app.logger.info("Supabase real-time features enabled")
        else:
            app.logger.warning("Using SQLite fallback mode")
    except Exception as e:
        app.logger.error(f"Supabase initialization failed: {e}")

# Authentication Routes (unchanged)
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

# Main game routes with Supabase
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
    
    if not current_user:
        session.clear()
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('login'))
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    # Get empire with real-time Supabase data
    empire = db.get_empire(current_user.empire_id)
    if not empire:
        return redirect(url_for('create_empire'))
    
    # Get all empires for the map (real-time)
    all_empires = db.get_all_empires()
    
    # Get recent events
    recent_events = db.get_recent_events(current_user.empire_id, 10)
    
    return render_template('dashboard.html', 
                         empire=asdict(empire), 
                         all_empires=[asdict(e) for e in all_empires],
                         recent_events=recent_events,
                         unit_costs=UNIT_COSTS,
                         unit_stats=UNIT_STATS)

@app.route('/create_empire', methods=['GET', 'POST'])
@login_required
def create_empire():
    current_user = get_current_user()
    
    if not current_user:
        session.clear()
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('login'))
    
    # Check if user already has an empire
    if current_user.empire_id:
        existing_empire = db.get_empire(current_user.empire_id)
        if existing_empire:
            return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            name = data.get('name', '').strip()
            ruler = data.get('ruler', '').strip()
            location_x = float(data.get('lat', 0))
            location_y = float(data.get('lng', 0))
        else:
            name = request.form.get('name', '').strip()
            ruler = request.form.get('ruler', '').strip()
            location_x = float(request.form.get('location_x', 0))
            location_y = float(request.form.get('location_y', 0))
        
        if not name or not ruler:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Empire name and ruler name are required'})
            flash('Empire name and ruler name are required', 'error')
            return render_template('create_empire.html')
        
        # Create the empire with Supabase real-time sync
        empire_id = db.create_empire(name, ruler, location_x, location_y)
        if empire_id:
            # Link the empire to the user
            auth_db.link_user_to_empire(current_user.id, empire_id)
            
            # Also link in Supabase if available
            if db.use_supabase:
                db.link_user_to_empire(current_user.id, empire_id)
            
            # Emit real-time empire creation event
            socketio.emit('empire_created', {
                'empire_id': empire_id,
                'name': name,
                'ruler': ruler,
                'location': {'lat': location_x, 'lng': location_y}
            }, room='game_room')
            
            if request.is_json:
                return jsonify({'success': True, 'message': f'Empire "{name}" created successfully!'})
            flash(f'Empire "{name}" created successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Empire name already exists. Please choose a different name.'})
            flash('Empire name already exists. Please choose a different name.', 'error')
    
    return render_template('create_empire.html')

@app.route('/military')
@login_required
def military():
    current_user = get_current_user()
    
    if not current_user:
        session.clear()
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('login'))
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    # Get real-time empire data
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
    
    if not current_user:
        session.clear()
        flash('Session expired. Please log in again.', 'warning')
        return redirect(url_for('login'))
    
    if not current_user.empire_id:
        return redirect(url_for('create_empire'))
    
    # Get real-time empire data
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
                         land_cost=LAND_COST_PER_ACRE,
                         building_types=BUILDING_TYPES)

# API Routes with Supabase real-time sync
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
    
    # Get real-time empire data
    empire = db.get_empire(current_user.empire_id)
    data = request.json
    
    total_cost = {'gold': 0, 'iron': 0, 'oil': 0, 'food': 0}
    
    # Calculate total cost
    for unit_type, count in data.items():
        if unit_type in UNIT_COSTS and count > 0:
            for resource, cost in UNIT_COSTS[unit_type].items():
                total_cost[resource] += cost * count
    
    # Check if empire has enough resources
    if (empire.resources.get('gold', 0) >= total_cost['gold'] and 
        empire.resources.get('iron', 0) >= total_cost['iron'] and 
        empire.resources.get('oil', 0) >= total_cost['oil'] and 
        empire.resources.get('food', 0) >= total_cost['food']):
        
        # Deduct resources
        empire.resources['gold'] -= total_cost['gold']
        empire.resources['iron'] -= total_cost['iron']
        empire.resources['oil'] -= total_cost['oil']
        empire.resources['food'] -= total_cost['food']
        
        # Add units
        for unit_type, count in data.items():
            if unit_type in UNIT_COSTS and count > 0:
                empire.military[unit_type] = empire.military.get(unit_type, 0) + count
        
        # Save to Supabase database (real-time sync)
        db.update_empire(empire)
        
        # Log resource transaction
        db.log_resource_transaction(
            empire.id, 'unit_training', total_cost, 
            f"Trained units: {', '.join([f'{count} {unit}' for unit, count in data.items() if count > 0])}"
        )
        
        # Emit real-time unit training update
        socketio.emit('units_trained', {
            'empire_id': empire.id,
            'units_trained': {unit: count for unit, count in data.items() if count > 0},
            'new_military': empire.military,
            'new_resources': empire.resources
        }, room='game_room')
        
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Insufficient resources'}), 400

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

@app.route('/api/attack', methods=['POST'])
@login_required
def attack():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    # Get real-time empire data
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
    if (attacking_units.get('infantry', 0) > attacker.military.get('infantry', 0) or
        attacking_units.get('tanks', 0) > attacker.military.get('tanks', 0) or
        attacking_units.get('aircraft', 0) > attacker.military.get('aircraft', 0) or
        attacking_units.get('ships', 0) > attacker.military.get('ships', 0)):
        return jsonify({'error': 'Insufficient units'}), 400
    
    # Execute battle with Supabase real-time updates
    result = battle_system.execute_battle(attacker, defender, attacking_units)
    
    # Update empires in Supabase database (real-time sync)
    db.update_empire(attacker)
    db.update_empire(defender)
    
    # Emit real-time battle updates via WebSocket
    socketio.emit('battle_update', {
        'battle_id': result['battle_id'],
        'attacker_id': attacker.id,
        'attacker_name': attacker.name,
        'defender_id': defender.id,
        'defender_name': defender.name,
        'result': result
    }, room='game_room')
    
    # Send battle notifications to specific empires
    socketio.emit('battle_notification', {
        'type': 'battle_result',
        'battle_id': result['battle_id'],
        'result': result,
        'message': f"Battle completed! {'Victory' if result['outcome']['attacker_wins'] else 'Defeat'}"
    }, room=f'empire_{attacker.id}')
    
    socketio.emit('battle_notification', {
        'type': 'under_attack',
        'battle_id': result['battle_id'],
        'result': result,
        'attacker_name': attacker.name,
        'message': f"Your empire was attacked by {attacker.name}! {'Defended successfully' if not result['outcome']['attacker_wins'] else 'Empire damaged'}"
    }, room=f'empire_{defender.id}')
    
    return jsonify(result)

@app.route('/api/send_message', methods=['POST'])
@login_required
def send_message():
    current_user = get_current_user()
    
    if not current_user.empire_id:
        return jsonify({'error': 'No empire found'}), 400
    
    data = request.json
    to_empire_id = data.get('to_empire_id')
    message = data.get('message', '').strip()
    message_type = data.get('message_type', 'general')
    
    if not to_empire_id or not message:
        return jsonify({'error': 'Recipient and message are required'}), 400
    
    # Send message with Supabase real-time sync
    message_id = db.send_message(current_user.empire_id, to_empire_id, message, message_type)
    
    # Get sender empire for notification
    sender_empire = db.get_empire(current_user.empire_id)
    
    # Emit real-time message notification
    socketio.emit('new_message', {
        'message_id': message_id,
        'from_empire_id': current_user.empire_id,
        'from_empire_name': sender_empire.name if sender_empire else 'Unknown',
        'to_empire_id': to_empire_id,
        'message': message,
        'message_type': message_type,
        'timestamp': datetime.now().isoformat()
    }, room=f'empire_{to_empire_id}')
    
    return jsonify({'success': True, 'message_id': message_id})

@app.route('/api/events/<empire_id>')
@login_required
def get_events(empire_id):
    current_user = get_current_user()
    
    # Only allow users to see their own events
    if current_user.empire_id != empire_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    events = db.get_recent_events(empire_id, 50)
    return jsonify({'events': events})

@app.route('/api/leaderboard')
def get_leaderboard():
    """Get empire leaderboard with real-time data"""
    try:
        all_empires = db.get_all_empires()
        
        # Calculate scores and sort
        leaderboard = []
        for empire in all_empires:
            if not empire.is_ai:  # Only include human players
                score = (
                    empire.land +
                    empire.resources.get('gold', 0) * 0.1 +
                    empire.calculate_military_power() * 10
                )
                
                leaderboard.append({
                    'id': empire.id,
                    'name': empire.name,
                    'ruler': empire.ruler,
                    'score': int(score),
                    'land': empire.land,
                    'military_power': empire.calculate_military_power(),
                    'gold': empire.resources.get('gold', 0)
                })
        
        # Sort by score descending
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({'leaderboard': leaderboard[:10]})  # Top 10
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# WebSocket events for real-time updates
@socketio.on('connect')
def on_connect():
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        join_room('game_room')
        join_room(f'empire_{current_user.empire_id}')
        
        # Get empire data for connection confirmation
        empire = db.get_empire(current_user.empire_id)
        
        emit('connected', {
            'status': 'Connected to Empire Builder with Supabase',
            'empire_id': current_user.empire_id,
            'empire_name': empire.name if empire else 'Unknown',
            'real_time_enabled': db.use_supabase
        })

@socketio.on('disconnect')
def on_disconnect():
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        leave_room('game_room')
        leave_room(f'empire_{current_user.empire_id}')

@socketio.on('subscribe_empire')
def on_subscribe_empire(data):
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        empire_id = data.get('empire_id')
        if empire_id == current_user.empire_id:
            join_room(f'empire_{empire_id}')
            emit('subscribed', {'empire_id': empire_id})

@socketio.on('request_empire_update')
def on_request_empire_update():
    """Send real-time empire update to client"""
    current_user = get_current_user()
    if current_user and current_user.empire_id:
        empire = db.get_empire(current_user.empire_id)
        if empire:
            emit('empire_update', {
                'empire': asdict(empire),
                'timestamp': datetime.now().isoformat()
            })

if __name__ == '__main__':
    # Initialize Supabase
    initialize_supabase_models()
    
    # Start the application
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    socketio.run(app, debug=debug_mode, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)