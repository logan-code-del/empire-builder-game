"""
Empire Builder Models with Supabase Integration
Real-time PostgreSQL database with advanced features
"""

import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from supabase_config import get_supabase_client, initialize_supabase
import sqlite3

# Game Configuration (unchanged)
STARTING_LAND = 2000
STARTING_RESOURCES = {
    'gold': 10000,
    'food': 5000,
    'iron': 2000,
    'oil': 1000,
    'population': 1000
}

# Building Configuration (unchanged)
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
        'cost': {'gold': 1000, 'iron': 150, 'population': 100},
        'production': {'gold': 50},
        'land_required': 8,
        'max_per_city': 3
    },
    'factory': {
        'name': 'Factory',
        'description': 'Increases population growth and unit production efficiency',
        'cost': {'gold': 2000, 'iron': 500, 'population': 200},
        'production': {'population': 10},
        'land_required': 25,
        'max_per_city': 2
    },
    'barracks': {
        'name': 'Barracks',
        'description': 'Reduces unit training costs and time',
        'cost': {'gold': 1500, 'iron': 400, 'population': 150},
        'production': {},
        'land_required': 20,
        'max_per_city': 2
    },
    'research_lab': {
        'name': 'Research Lab',
        'description': 'Unlocks advanced technologies and unit upgrades',
        'cost': {'gold': 3000, 'iron': 600, 'population': 300},
        'production': {},
        'land_required': 30,
        'max_per_city': 1
    },
    'hospital': {
        'name': 'Hospital',
        'description': 'Reduces casualty rates in battles and increases population growth',
        'cost': {'gold': 2500, 'iron': 300, 'population': 250},
        'production': {'population': 15},
        'land_required': 15,
        'max_per_city': 2
    }
}

# City Configuration (unchanged)
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

LAND_COST_PER_ACRE = 10

# Unit Configuration (unchanged)
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
    """Empire class with Supabase integration"""
    id: str
    name: str
    ruler: str
    land: int
    resources: Dict[str, int]
    military: Dict[str, int]
    location: Dict[str, float]
    last_update: str
    is_ai: bool = False
    cities: Dict[str, Dict] = None
    buildings: Dict[str, int] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.cities is None:
            self.cities = {}
        if self.buildings is None:
            self.buildings = {building_type: 0 for building_type in BUILDING_TYPES.keys()}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()
    
    def calculate_military_power(self) -> int:
        """Calculate total military power"""
        total_power = 0
        for unit_type, count in self.military.items():
            if unit_type in UNIT_STATS:
                unit_power = (UNIT_STATS[unit_type]['attack'] + UNIT_STATS[unit_type]['defense']) / 2
                total_power += unit_power * count
        return int(total_power)

class SupabaseGameDatabase:
    """Game database with Supabase real-time integration"""
    
    def __init__(self):
        self.supabase = None
        self.use_supabase = False
        self.fallback_db = 'empire_game.db'
        
    def initialize(self):
        """Initialize Supabase connection"""
        try:
            if initialize_supabase():
                self.supabase = get_supabase_client()
                self.use_supabase = True
                print("Using Supabase for real-time features")
            else:
                print("Using SQLite fallback mode")
                self.use_supabase = False
        except Exception as e:
            print(f"Supabase initialization failed: {e}")
            self.use_supabase = False
    
    def _get_fallback_connection(self):
        """Get SQLite fallback connection"""
        return sqlite3.connect(self.fallback_db)
    
    def create_empire(self, name: str, ruler: str, lat: float, lng: float) -> str:
        """Create a new empire with Supabase real-time sync"""
        empire_id = str(uuid.uuid4())
        
        if self.use_supabase and self.supabase:
            try:
                # Create empire in Supabase
                response = self.supabase.table('empires').insert({
                    'id': empire_id,
                    'name': name,
                    'ruler': ruler,
                    'land': STARTING_LAND,
                    'resources': STARTING_RESOURCES,
                    'military': {'infantry': 100, 'tanks': 10, 'aircraft': 5, 'ships': 8},
                    'location': {'lat': lat, 'lng': lng},
                    'is_ai': False,
                    'cities': {},
                    'buildings': {building_type: 0 for building_type in BUILDING_TYPES.keys()}
                }).execute()
                
                if response.data:
                    # Log empire creation event
                    self.log_game_event(empire_id, 'empire_created', {
                        'empire_name': name,
                        'ruler': ruler,
                        'location': {'lat': lat, 'lng': lng}
                    })
                    
                    print(f"Empire created in Supabase: {name}")
                    return empire_id
                else:
                    raise Exception("Failed to create empire in Supabase")
                    
            except Exception as e:
                print(f"Supabase empire creation failed: {e}")
                # Fall back to SQLite
                return self._create_empire_fallback(empire_id, name, ruler, lat, lng)
        else:
            return self._create_empire_fallback(empire_id, name, ruler, lat, lng)
    
    def _create_empire_fallback(self, empire_id: str, name: str, ruler: str, lat: float, lng: float) -> str:
        """Create empire in SQLite fallback"""
        conn = self._get_fallback_connection()
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
            json.dumps({}),
            json.dumps({building_type: 0 for building_type in BUILDING_TYPES.keys()})
        ))
        
        conn.commit()
        conn.close()
        
        print(f"Empire created in SQLite: {name}")
        return empire_id
    
    def get_empire(self, empire_id: str) -> Optional[Empire]:
        """Get empire with real-time data"""
        if self.use_supabase and self.supabase:
            try:
                # Update resources first
                self.supabase.rpc('update_empire_resources', {'empire_id': empire_id}).execute()
                
                # Get empire data
                response = self.supabase.table('empires').select('*').eq('id', empire_id).execute()
                
                if response.data:
                    empire_data = response.data[0]
                    return Empire(
                        id=empire_data['id'],
                        name=empire_data['name'],
                        ruler=empire_data['ruler'],
                        land=empire_data['land'],
                        resources=empire_data['resources'],
                        military=empire_data['military'],
                        location=empire_data['location'],
                        last_update=empire_data['last_update'],
                        is_ai=empire_data['is_ai'],
                        cities=empire_data['cities'],
                        buildings=empire_data['buildings'],
                        created_at=empire_data['created_at'],
                        updated_at=empire_data['updated_at']
                    )
            except Exception as e:
                print(f"Supabase get_empire failed: {e}")
                # Fall back to SQLite
                return self._get_empire_fallback(empire_id)
        else:
            return self._get_empire_fallback(empire_id)
        
        return None
    
    def _get_empire_fallback(self, empire_id: str) -> Optional[Empire]:
        """Get empire from SQLite fallback"""
        conn = self._get_fallback_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM empires WHERE id = ?', (empire_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            empire_data = dict(zip(columns, row))
            
            return Empire(
                id=empire_data['id'],
                name=empire_data['name'],
                ruler=empire_data['ruler'],
                land=empire_data['land'],
                resources=json.loads(empire_data['resources']),
                military=json.loads(empire_data['military']),
                location=json.loads(empire_data['location']),
                last_update=empire_data['last_update'],
                is_ai=empire_data.get('is_ai', False),
                cities=json.loads(empire_data.get('cities', '{}')),
                buildings=json.loads(empire_data.get('buildings', '{}'))
            )
        
        return None
    
    def update_empire(self, empire: Empire) -> bool:
        """Update empire with Supabase real-time sync"""
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('empires').update({
                    'land': empire.land,
                    'resources': empire.resources,
                    'military': empire.military,
                    'location': empire.location,
                    'last_update': empire.last_update,
                    'cities': empire.cities,
                    'buildings': empire.buildings,
                    'updated_at': datetime.now().isoformat()
                }).eq('id', empire.id).execute()
                
                if response.data:
                    print(f"Empire updated in Supabase: {empire.id}")
                    return True
                else:
                    raise Exception("Failed to update empire in Supabase")
                    
            except Exception as e:
                print(f"Supabase update_empire failed: {e}")
                # Fall back to SQLite
                return self._update_empire_fallback(empire)
        else:
            return self._update_empire_fallback(empire)
    
    def _update_empire_fallback(self, empire: Empire) -> bool:
        """Update empire in SQLite fallback"""
        conn = self._get_fallback_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE empires SET 
                land = ?, resources = ?, military = ?, location = ?, 
                last_update = ?, cities = ?, buildings = ?
            WHERE id = ?
        ''', (
            empire.land,
            json.dumps(empire.resources),
            json.dumps(empire.military),
            json.dumps(empire.location),
            empire.last_update,
            json.dumps(empire.cities),
            json.dumps(empire.buildings),
            empire.id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            print(f"Empire updated in SQLite: {empire.id}")
        
        return success
    
    def get_all_empires(self) -> List[Empire]:
        """Get all empires with real-time data"""
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('empires').select('*').order('created_at', desc=True).execute()
                
                empires = []
                for empire_data in response.data:
                    empire = Empire(
                        id=empire_data['id'],
                        name=empire_data['name'],
                        ruler=empire_data['ruler'],
                        land=empire_data['land'],
                        resources=empire_data['resources'],
                        military=empire_data['military'],
                        location=empire_data['location'],
                        last_update=empire_data['last_update'],
                        is_ai=empire_data['is_ai'],
                        cities=empire_data['cities'],
                        buildings=empire_data['buildings'],
                        created_at=empire_data['created_at'],
                        updated_at=empire_data['updated_at']
                    )
                    empires.append(empire)
                
                return empires
                
            except Exception as e:
                print(f"Supabase get_all_empires failed: {e}")
                # Fall back to SQLite
                return self._get_all_empires_fallback()
        else:
            return self._get_all_empires_fallback()
    
    def _get_all_empires_fallback(self) -> List[Empire]:
        """Get all empires from SQLite fallback"""
        conn = self._get_fallback_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM empires ORDER BY last_update DESC')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        empires = []
        for row in rows:
            empire_data = dict(zip(columns, row))
            empire = Empire(
                id=empire_data['id'],
                name=empire_data['name'],
                ruler=empire_data['ruler'],
                land=empire_data['land'],
                resources=json.loads(empire_data['resources']),
                military=json.loads(empire_data['military']),
                location=json.loads(empire_data['location']),
                last_update=empire_data['last_update'],
                is_ai=empire_data.get('is_ai', False),
                cities=json.loads(empire_data.get('cities', '{}')),
                buildings=json.loads(empire_data.get('buildings', '{}'))
            )
            empires.append(empire)
        
        return empires
    
    def create_battle(self, attacker_id: str, defender_id: str, attacking_units: Dict) -> str:
        """Create a battle with Supabase real-time sync"""
        battle_id = str(uuid.uuid4())
        
        # Get defender's units
        defender = self.get_empire(defender_id)
        defending_units = defender.military if defender else {}
        
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('battles').insert({
                    'id': battle_id,
                    'attacker_id': attacker_id,
                    'defender_id': defender_id,
                    'attacking_units': attacking_units,
                    'defending_units': defending_units,
                    'status': 'active'
                }).execute()
                
                if response.data:
                    # Log battle event
                    self.log_game_event(attacker_id, 'battle_started', {
                        'defender_id': defender_id,
                        'battle_id': battle_id,
                        'attacking_units': attacking_units
                    })
                    
                    print(f"Battle created in Supabase: {battle_id}")
                    return battle_id
                else:
                    raise Exception("Failed to create battle in Supabase")
                    
            except Exception as e:
                print(f"Supabase create_battle failed: {e}")
                # Could implement SQLite fallback here if needed
                
        return battle_id
    
    def complete_battle(self, battle_id: str, result: Dict) -> bool:
        """Complete a battle with results"""
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('battles').update({
                    'result': result.get('outcome', {}),
                    'casualties': result.get('casualties', {}),
                    'resources_gained': result.get('resources_gained', {}),
                    'land_gained': result.get('land_gained', 0),
                    'status': 'completed',
                    'completed_at': datetime.now().isoformat()
                }).eq('id', battle_id).execute()
                
                if response.data:
                    print(f"Battle completed in Supabase: {battle_id}")
                    return True
                    
            except Exception as e:
                print(f"Supabase complete_battle failed: {e}")
        
        return False
    
    def send_message(self, from_empire_id: str, to_empire_id: str, message: str, message_type: str = 'general') -> str:
        """Send a message with Supabase real-time sync"""
        message_id = str(uuid.uuid4())
        
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('messages').insert({
                    'id': message_id,
                    'from_empire': from_empire_id,
                    'to_empire': to_empire_id,
                    'message': message,
                    'message_type': message_type,
                    'read': False
                }).execute()
                
                if response.data:
                    print(f"Message sent via Supabase: {from_empire_id} -> {to_empire_id}")
                    return message_id
                    
            except Exception as e:
                print(f"Supabase send_message failed: {e}")
        
        return message_id
    
    def log_game_event(self, empire_id: str, event_type: str, event_data: Dict) -> str:
        """Log a game event with Supabase real-time sync"""
        event_id = str(uuid.uuid4())
        
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('game_events').insert({
                    'id': event_id,
                    'empire_id': empire_id,
                    'event_type': event_type,
                    'event_data': event_data
                }).execute()
                
                if response.data:
                    return event_id
                    
            except Exception as e:
                print(f"Supabase log_game_event failed: {e}")
        
        return event_id
    
    def log_resource_transaction(self, empire_id: str, transaction_type: str, resources: Dict, reason: str) -> str:
        """Log a resource transaction with Supabase real-time sync"""
        transaction_id = str(uuid.uuid4())
        
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('resource_transactions').insert({
                    'id': transaction_id,
                    'empire_id': empire_id,
                    'transaction_type': transaction_type,
                    'resources': resources,
                    'reason': reason
                }).execute()
                
                if response.data:
                    return transaction_id
                    
            except Exception as e:
                print(f"Supabase log_resource_transaction failed: {e}")
        
        return transaction_id
    
    def get_recent_events(self, empire_id: str = None, limit: int = 50) -> List[Dict]:
        """Get recent game events"""
        if self.use_supabase and self.supabase:
            try:
                query = self.supabase.table('game_events').select('*')
                
                if empire_id:
                    query = query.eq('empire_id', empire_id)
                
                response = query.order('created_at', desc=True).limit(limit).execute()
                
                return response.data if response.data else []
                
            except Exception as e:
                print(f"Supabase get_recent_events failed: {e}")
        
        return []
    
    def link_user_to_empire(self, user_id: str, empire_id: str) -> bool:
        """Link a user to an empire"""
        if self.use_supabase and self.supabase:
            try:
                response = self.supabase.table('user_empires').insert({
                    'user_id': user_id,
                    'empire_id': empire_id
                }).execute()
                
                return bool(response.data)
                
            except Exception as e:
                print(f"Supabase link_user_to_empire failed: {e}")
        
        return False

class SupabaseBattleSystem:
    """Enhanced battle system with Supabase real-time integration"""
    
    def __init__(self, db: SupabaseGameDatabase):
        self.db = db
    
    def execute_battle(self, attacker: Empire, defender: Empire, attacking_units: Dict) -> Dict:
        """Execute battle with real-time updates"""
        
        # Create battle record
        battle_id = self.db.create_battle(attacker.id, defender.id, attacking_units)
        
        # Calculate battle outcome
        attacker_power = self.calculate_army_power(attacking_units)
        defender_power = self.calculate_army_power(defender.military)
        
        # Apply city defense bonuses
        city_defense_bonus = 1.0
        for city_data in defender.cities.values():
            city_type = city_data.get('type', 'small')
            city_defense_bonus += CITY_STATS[city_type]['defense_bonus'] - 1.0
        
        defender_power *= city_defense_bonus
        
        # Determine winner
        total_power = attacker_power + defender_power
        attacker_win_chance = attacker_power / total_power if total_power > 0 else 0.5
        
        import random
        attacker_wins = random.random() < attacker_win_chance
        
        # Calculate casualties
        casualty_rate = 0.1 + (0.3 * min(attacker_power, defender_power) / max(attacker_power, defender_power))
        
        attacker_casualties = {}
        defender_casualties = {}
        
        # Apply casualties to attacker
        for unit_type, count in attacking_units.items():
            casualties = int(count * casualty_rate * random.uniform(0.5, 1.5))
            casualties = min(casualties, count)
            attacker_casualties[unit_type] = casualties
            attacker.military[unit_type] -= casualties
        
        # Apply casualties to defender
        for unit_type, count in defender.military.items():
            if count > 0:
                casualties = int(count * casualty_rate * random.uniform(0.5, 1.5))
                casualties = min(casualties, count)
                defender_casualties[unit_type] = casualties
                defender.military[unit_type] -= casualties
        
        # Determine spoils of war
        resources_gained = {}
        land_gained = 0
        
        if attacker_wins:
            # Attacker gains resources and land
            for resource in ['gold', 'food', 'iron', 'oil']:
                amount = int(defender.resources.get(resource, 0) * 0.1)
                resources_gained[resource] = amount
                attacker.resources[resource] += amount
                defender.resources[resource] -= amount
            
            land_gained = int(defender.land * 0.05)
            attacker.land += land_gained
            defender.land -= land_gained
        
        # Battle result
        result = {
            'battle_id': battle_id,
            'outcome': {
                'winner': attacker.id if attacker_wins else defender.id,
                'attacker_wins': attacker_wins
            },
            'casualties': {
                'attacker': attacker_casualties,
                'defender': defender_casualties
            },
            'resources_gained': resources_gained,
            'land_gained': land_gained,
            'attacker_power': attacker_power,
            'defender_power': defender_power
        }
        
        # Complete battle in Supabase
        self.db.complete_battle(battle_id, result)
        
        # Log battle events
        self.db.log_game_event(attacker.id, 'battle_completed', {
            'battle_id': battle_id,
            'result': 'victory' if attacker_wins else 'defeat',
            'defender_id': defender.id
        })
        
        self.db.log_game_event(defender.id, 'battle_completed', {
            'battle_id': battle_id,
            'result': 'victory' if not attacker_wins else 'defeat',
            'attacker_id': attacker.id
        })
        
        return result
    
    def calculate_army_power(self, units: Dict) -> float:
        """Calculate total army power"""
        total_power = 0
        for unit_type, count in units.items():
            if unit_type in UNIT_STATS and count > 0:
                unit_power = (UNIT_STATS[unit_type]['attack'] + UNIT_STATS[unit_type]['defense']) / 2
                total_power += unit_power * count
        return total_power

# Global instances
supabase_db = SupabaseGameDatabase()
supabase_battle_system = SupabaseBattleSystem(supabase_db)

def initialize_supabase_models():
    """Initialize Supabase models"""
    supabase_db.initialize()
    return supabase_db.use_supabase