"""
Empire Builder - Data Models and Game Logic
Contains core game classes and database operations
"""

import sqlite3
import json
import random
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

# Game Configuration
STARTING_LAND = 2000  # square acres
STARTING_RESOURCES = {
    'gold': 10000,
    'food': 5000,
    'iron': 2000,
    'oil': 1000,
    'population': 1000
}

# Building Configuration
BUILDING_TYPES = {
    'farm': {
        'name': 'Farm',
        'description': 'Increases food production',
        'cost': {'gold': 500, 'iron': 100, 'population': 50},
        'production': {'food': 25},
        'land_required': 10,
        'max_per_city': 5
    },
    'mine': {
        'name': 'Mine',
        'description': 'Increases iron production',
        'cost': {'gold': 800, 'iron': 200, 'population': 75},
        'production': {'iron': 15},
        'land_required': 15,
        'max_per_city': 3
    },
    'oil_well': {
        'name': 'Oil Well',
        'description': 'Increases oil production',
        'cost': {'gold': 1200, 'iron': 300, 'population': 100},
        'production': {'oil': 10},
        'land_required': 20,
        'max_per_city': 2
    },
    'bank': {
        'name': 'Bank',
        'description': 'Increases gold production',
        'cost': {'gold': 1000, 'population': 150},
        'production': {'gold': 50},
        'land_required': 5,
        'max_per_city': 2
    },
    'housing': {
        'name': 'Housing Complex',
        'description': 'Increases population growth',
        'cost': {'gold': 600, 'iron': 150, 'food': 200},
        'production': {'population': 20},
        'land_required': 8,
        'max_per_city': 10
    },
    'factory': {
        'name': 'Factory',
        'description': 'Boosts overall production efficiency',
        'cost': {'gold': 2000, 'iron': 500, 'oil': 200, 'population': 200},
        'production': {'gold': 30, 'iron': 10, 'food': 15},
        'land_required': 25,
        'max_per_city': 1
    }
}

# City Configuration
CITY_COSTS = {
    'small': {'gold': 5000, 'population': 500, 'land': 100},
    'medium': {'gold': 15000, 'population': 1500, 'land': 250},
    'large': {'gold': 40000, 'population': 4000, 'land': 500}
}

CITY_STATS = {
    'small': {'max_buildings': 15, 'defense_bonus': 1.1, 'production_bonus': 1.0},
    'medium': {'max_buildings': 35, 'defense_bonus': 1.2, 'production_bonus': 1.1},
    'large': {'max_buildings': 60, 'defense_bonus': 1.3, 'production_bonus': 1.2}
}

# Land expansion costs (per acre)
LAND_COST_PER_ACRE = 10  # Gold cost per acre

UNIT_COSTS = {
    'infantry': {'gold': 100, 'iron': 50, 'food': 20},
    'tanks': {'gold': 500, 'iron': 300, 'oil': 100},
    'aircraft': {'gold': 1000, 'iron': 400, 'oil': 200},
    'ships': {'gold': 800, 'iron': 500, 'oil': 150}
}

UNIT_STATS = {
    'infantry': {'attack': 10, 'defense': 15, 'speed': 5},
    'tanks': {'attack': 25, 'defense': 20, 'speed': 8},
    'aircraft': {'attack': 30, 'defense': 10, 'speed': 15},
    'ships': {'attack': 20, 'defense': 25, 'speed': 6}
}

@dataclass
class Empire:
    id: str
    name: str
    ruler: str
    land: int
    resources: Dict[str, int]
    military: Dict[str, int]
    location: Dict[str, float]  # lat, lng
    last_update: str
    is_ai: bool = False
    cities: Dict[str, Dict] = None  # city_id -> {name, type, buildings}
    buildings: Dict[str, int] = None  # building_type -> count
    
    def __post_init__(self):
        if self.cities is None:
            self.cities = {}
        if self.buildings is None:
            self.buildings = {building_type: 0 for building_type in BUILDING_TYPES.keys()}

class GameDatabase:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        # Empires table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empires (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                ruler TEXT NOT NULL,
                land INTEGER DEFAULT 2000,
                resources TEXT DEFAULT '{}',
                military TEXT DEFAULT '{}',
                location TEXT DEFAULT '{}',
                last_update TEXT,
                is_ai BOOLEAN DEFAULT 0,
                cities TEXT DEFAULT '{}',
                buildings TEXT DEFAULT '{}'
            )
        ''')
        
        # Add new columns if they don't exist (migration)
        try:
            cursor.execute('ALTER TABLE empires ADD COLUMN cities TEXT DEFAULT "{}"')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute('ALTER TABLE empires ADD COLUMN buildings TEXT DEFAULT "{}"')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Battles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS battles (
                id TEXT PRIMARY KEY,
                attacker_id TEXT,
                defender_id TEXT,
                battle_data TEXT,
                result TEXT,
                timestamp TEXT,
                FOREIGN KEY (attacker_id) REFERENCES empires (id),
                FOREIGN KEY (defender_id) REFERENCES empires (id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                from_empire TEXT,
                to_empire TEXT,
                message TEXT,
                timestamp TEXT,
                read BOOLEAN DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_empire(self, name: str, ruler: str, lat: float, lng: float) -> str:
        empire_id = str(uuid.uuid4())
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO empires (id, name, ruler, land, resources, military, location, last_update, cities, buildings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            empire_id, name, ruler, STARTING_LAND,
            json.dumps(STARTING_RESOURCES),
            json.dumps({'infantry': 100, 'tanks': 10, 'aircraft': 5, 'ships': 8}),
            json.dumps({'lat': lat, 'lng': lng}),
            datetime.now().isoformat(),
            json.dumps({}),  # cities
            json.dumps({building_type: 0 for building_type in BUILDING_TYPES.keys()})  # buildings
        ))
        
        conn.commit()
        conn.close()
        return empire_id
    
    def get_empire(self, empire_id: str) -> Optional[Empire]:
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM empires WHERE id = ?', (empire_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            cities = json.loads(row[9]) if len(row) > 9 and row[9] else {}
            buildings = json.loads(row[10]) if len(row) > 10 and row[10] else {}
            
            # Ensure all building types are present (for existing empires)
            for building_type in BUILDING_TYPES.keys():
                if building_type not in buildings:
                    buildings[building_type] = 0
            
            return Empire(
                id=row[0],
                name=row[1],
                ruler=row[2],
                land=row[3],
                resources=json.loads(row[4]),
                military=json.loads(row[5]),
                location=json.loads(row[6]),
                last_update=row[7],
                is_ai=bool(row[8]),
                cities=cities,
                buildings=buildings
            )
        return None
    
    def get_all_empires(self) -> List[Empire]:
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM empires')
        rows = cursor.fetchall()
        conn.close()
        
        empires = []
        for row in rows:
            cities = json.loads(row[9]) if len(row) > 9 and row[9] else {}
            buildings = json.loads(row[10]) if len(row) > 10 and row[10] else {}
            
            # Ensure all building types are present (for existing empires)
            for building_type in BUILDING_TYPES.keys():
                if building_type not in buildings:
                    buildings[building_type] = 0
            
            empires.append(Empire(
                id=row[0],
                name=row[1],
                ruler=row[2],
                land=row[3],
                resources=json.loads(row[4]),
                military=json.loads(row[5]),
                location=json.loads(row[6]),
                last_update=row[7],
                is_ai=bool(row[8]),
                cities=cities,
                buildings=buildings
            ))
        return empires
    
    def update_empire(self, empire: Empire):
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE empires SET name=?, ruler=?, land=?, resources=?, military=?, 
                             location=?, last_update=?, cities=?, buildings=? WHERE id=?
        ''', (
            empire.name, empire.ruler, empire.land,
            json.dumps(empire.resources),
            json.dumps(empire.military),
            json.dumps(empire.location),
            datetime.now().isoformat(),
            json.dumps(empire.cities),
            json.dumps(empire.buildings),
            empire.id
        ))
        
        conn.commit()
        conn.close()
    
    def build_city(self, empire: Empire, city_name: str, city_type: str) -> bool:
        """Build a new city"""
        if city_type not in CITY_COSTS:
            return False
        
        costs = CITY_COSTS[city_type]
        
        # Check if empire can afford it
        for resource, cost in costs.items():
            if resource == 'land':
                if empire.land < cost:
                    return False
            else:
                if empire.resources.get(resource, 0) < cost:
                    return False
        
        # Deduct costs
        for resource, cost in costs.items():
            if resource == 'land':
                empire.land -= cost
            else:
                empire.resources[resource] -= cost
        
        # Create city
        city_id = str(uuid.uuid4())
        empire.cities[city_id] = {
            'name': city_name,
            'type': city_type,
            'buildings': {building_type: 0 for building_type in BUILDING_TYPES.keys()}
        }
        
        self.update_empire(empire)
        return True
    
    def build_building(self, empire: Empire, city_id: str, building_type: str) -> bool:
        """Build a building in a city"""
        if city_id not in empire.cities or building_type not in BUILDING_TYPES:
            return False
        
        # Ensure empire buildings dictionary is properly initialized
        if empire.buildings is None:
            empire.buildings = {bt: 0 for bt in BUILDING_TYPES.keys()}
        
        # Ensure all building types exist in the dictionary
        for bt in BUILDING_TYPES.keys():
            if bt not in empire.buildings:
                empire.buildings[bt] = 0
        
        city = empire.cities[city_id]
        building_config = BUILDING_TYPES[building_type]
        
        # Check building limits
        current_count = city['buildings'].get(building_type, 0)
        if current_count >= building_config['max_per_city']:
            return False
        
        # Check city capacity
        total_buildings = sum(city['buildings'].values())
        max_buildings = CITY_STATS[city['type']]['max_buildings']
        if total_buildings >= max_buildings:
            return False
        
        # Check land requirements
        land_needed = building_config['land_required']
        if empire.land < land_needed:
            return False
        
        # Check costs
        for resource, cost in building_config['cost'].items():
            if empire.resources.get(resource, 0) < cost:
                return False
        
        # Deduct costs
        for resource, cost in building_config['cost'].items():
            empire.resources[resource] -= cost
        
        # Use land
        empire.land -= land_needed
        
        # Add building
        city['buildings'][building_type] += 1
        empire.buildings[building_type] += 1
        
        self.update_empire(empire)
        return True
    
    def buy_land(self, empire: Empire, acres: int) -> bool:
        """Buy additional land"""
        total_cost = acres * LAND_COST_PER_ACRE
        
        if empire.resources.get('gold', 0) < total_cost:
            return False
        
        empire.resources['gold'] -= total_cost
        empire.land += acres
        
        self.update_empire(empire)
        return True
    
    def calculate_building_production(self, empire: Empire) -> Dict[str, int]:
        """Calculate total production from all buildings"""
        total_production = {'gold': 0, 'food': 0, 'iron': 0, 'oil': 0, 'population': 0}
        
        # Safety check for cities
        if not empire.cities:
            return total_production
        
        for city_id, city in empire.cities.items():
            city_type = city['type']
            production_bonus = CITY_STATS[city_type]['production_bonus']
            
            for building_type, count in city['buildings'].items():
                if count > 0 and building_type in BUILDING_TYPES:
                    building_production = BUILDING_TYPES[building_type]['production']
                    for resource, amount in building_production.items():
                        total_production[resource] += int(amount * count * production_bonus)
        
        return total_production

class BattleSystem:
    @staticmethod
    def calculate_battle(attacker: Empire, defender: Empire, attacking_units: Dict[str, int]) -> Dict:
        """Calculate battle results using real-time combat simulation"""
        
        # Calculate total attack and defense power
        attacker_power = 0
        for unit_type, count in attacking_units.items():
            if count > 0 and unit_type in UNIT_STATS:
                attacker_power += count * UNIT_STATS[unit_type]['attack']
        
        defender_power = 0
        for unit_type, count in defender.military.items():
            if count > 0 and unit_type in UNIT_STATS:
                defender_power += count * UNIT_STATS[unit_type]['defense']
        
        # Add randomness and terrain bonuses
        attacker_power *= random.uniform(0.8, 1.2)
        defender_power *= random.uniform(0.9, 1.3)  # Defender advantage
        
        # Determine winner
        if attacker_power > defender_power:
            victory_ratio = min(attacker_power / defender_power, 2.0)
            land_captured = min(int(defender.land * 0.1 * victory_ratio), defender.land // 2)
            resources_captured = {}
            
            for resource, amount in defender.resources.items():
                captured = int(amount * 0.05 * victory_ratio)
                resources_captured[resource] = captured
                defender.resources[resource] -= captured
                attacker.resources[resource] = attacker.resources.get(resource, 0) + captured
            
            # Calculate losses
            attacker_losses = {}
            defender_losses = {}
            
            for unit_type, count in attacking_units.items():
                loss_rate = random.uniform(0.1, 0.3)
                losses = int(count * loss_rate)
                attacker_losses[unit_type] = losses
                attacker.military[unit_type] -= losses
            
            for unit_type, count in defender.military.items():
                loss_rate = random.uniform(0.2, 0.5)
                losses = int(count * loss_rate)
                defender_losses[unit_type] = losses
                defender.military[unit_type] = max(0, count - losses)
            
            # Transfer land
            attacker.land += land_captured
            defender.land -= land_captured
            
            return {
                'winner': 'attacker',
                'attacker_id': attacker.id,
                'defender_id': defender.id,
                'land_captured': land_captured,
                'resources_captured': resources_captured,
                'attacker_losses': attacker_losses,
                'defender_losses': defender_losses,
                'battle_power': {'attacker': int(attacker_power), 'defender': int(defender_power)}
            }
        else:
            # Defender wins
            victory_ratio = min(defender_power / attacker_power, 2.0)
            
            # Heavy attacker losses
            attacker_losses = {}
            for unit_type, count in attacking_units.items():
                loss_rate = random.uniform(0.4, 0.7)
                losses = int(count * loss_rate)
                attacker_losses[unit_type] = losses
                attacker.military[unit_type] -= losses
            
            # Light defender losses
            defender_losses = {}
            for unit_type, count in defender.military.items():
                loss_rate = random.uniform(0.05, 0.15)
                losses = int(count * loss_rate)
                defender_losses[unit_type] = losses
                defender.military[unit_type] = max(0, count - losses)
            
            return {
                'winner': 'defender',
                'attacker_id': attacker.id,
                'defender_id': defender.id,
                'land_captured': 0,
                'resources_captured': {},
                'attacker_losses': attacker_losses,
                'defender_losses': defender_losses,
                'battle_power': {'attacker': int(attacker_power), 'defender': int(defender_power)}
            }