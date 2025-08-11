"""
Empire Builder - Main Flask Application
A comprehensive web-based empire building strategy game
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import time
import threading
from dataclasses import asdict

# Import our models and game logic
from models import GameDatabase, Empire, BattleSystem, UNIT_COSTS, UNIT_STATS
from ai_system import ai_manager, create_ai_empires, initialize_ai_system

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'empire-builder-secret-key-2024')
socketio = SocketIO(app, cors_allowed_origins="*")

# Global game state
db = GameDatabase()
active_battles = {}  # battle_id -> battle_data

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_empire', methods=['GET', 'POST'])
def create_empire():
    if request.method == 'POST':
        data = request.json
        empire_id = db.create_empire(
            data['name'], 
            data['ruler'], 
            data['lat'], 
            data['lng']
        )
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
def dashboard():
    if 'empire_id' not in session:
        return redirect(url_for('index'))
    
    empire = db.get_empire(session['empire_id'])
    if not empire:
        return redirect(url_for('index'))
    
    return render_template('dashboard.html', empire=asdict(empire))

@app.route('/world_map')
def world_map():
    if 'empire_id' not in session:
        return redirect(url_for('index'))
    
    empires = db.get_all_empires()
    return render_template('world_map.html', empires=[asdict(e) for e in empires])

@app.route('/military')
def military():
    if 'empire_id' not in session:
        return redirect(url_for('index'))
    
    empire = db.get_empire(session['empire_id'])
    return render_template('military.html', empire=asdict(empire), unit_costs=UNIT_COSTS, unit_stats=UNIT_STATS)

@app.route('/cities')
def cities():
    if 'empire_id' not in session:
        return redirect(url_for('index'))
    
    empire = db.get_empire(session['empire_id'])
    from models import BUILDING_TYPES, CITY_COSTS, CITY_STATS, LAND_COST_PER_ACRE
    
    return render_template('cities.html', 
                         empire=asdict(empire), 
                         building_types=BUILDING_TYPES,
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
def train_units():
    if 'empire_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    empire = db.get_empire(session['empire_id'])
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
def attack_empire():
    if 'empire_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    attacker = db.get_empire(session['empire_id'])
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
def build_city():
    if 'empire_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    empire = db.get_empire(session['empire_id'])
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
def build_building():
    if 'empire_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    empire = db.get_empire(session['empire_id'])
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
def buy_land():
    if 'empire_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    empire = db.get_empire(session['empire_id'])
    data = request.json
    
    acres = data.get('acres', 0)
    
    if acres <= 0:
        return jsonify({'error': 'Invalid land amount'}), 400
    
    if db.buy_land(empire, acres):
        return jsonify({'success': True, 'empire': asdict(empire)})
    else:
        return jsonify({'error': 'Insufficient gold'}), 400

# Socket.IO events for real-time features
@socketio.on('connect')
def on_connect():
    if 'empire_id' in session:
        join_room(f'empire_{session["empire_id"]}')
        emit('connected', {'status': 'Connected to Empire Builder'})

@socketio.on('disconnect')
def on_disconnect():
    if 'empire_id' in session:
        leave_room(f'empire_{session["empire_id"]}')

@socketio.on('join_empire')
def on_join_empire(data):
    empire_id = data['empire_id']
    join_room(f'empire_{empire_id}')
    session['empire_id'] = empire_id

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