"""
Empire Builder Models with Electric-SQL Integration
Enhanced with real-time synchronization capabilities
"""

import json
import sqlite3
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from electric_bridge import electric_bridge

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
    """Empire class with Electric-SQL integration"""
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
    
    def update_resources(self):
        """Update resources based on buildings and time passed"""
        now = datetime.now()
        last_update = datetime.fromisoformat(self.last_update)
        hours_passed = (now - last_update).total_seconds() / 3600
        
        if hours_passed < 0.1:  # Less than 6 minutes
            return
        
        # Base production rates
        base_production = {
            'gold': 100,
            'food': 50,
            'iron': 25,
            'oil': 15,
            'population': 5
        }
        
        # Calculate building bonuses
        building_production = {'gold': 0, 'food': 0, 'iron': 0, 'oil': 0, 'population': 0}
        
        for building_type, count in self.buildings.items():
            if count > 0 and building_type in BUILDING_TYPES:
                building_config = BUILDING_TYPES[building_type]
                for resource, amount in building_config['production'].items():
                    building_production[resource] += amount * count
        
        # Apply city bonuses
        city_bonus = 1.0
        for city_data in self.cities.values():
            city_type = city_data.get('type', 'small')
            if city_type in CITY_STATS:
                city_bonus += CITY_STATS[city_type]['production_bonus']
        
        # Update resources
        for resource in base_production:
            total_production = (base_production[resource] + building_production[resource]) * city_bonus
            self.resources[resource] += int(total_production * hours_passed)
        
        # Ensure resources don't go negative
        for resource in self.resources:
            self.resources[resource] = max(0, self.resources[resource])
        
        self.last_update = now.isoformat()
        
        # Log resource transaction
        electric_bridge.log_resource_transaction(
            self.id, 'production', 
            {k: int(v * hours_passed) for k, v in building_production.items()},
            f'Hourly production over {hours_passed:.1f} hours'
        )
    
    def calculate_military_power(self) -> int:
        """Calculate total military power"""
        total_power = 0
        for unit_type, count in self.military.items():
            if unit_type in UNIT_STATS:
                unit_power = (UNIT_STATS[unit_type]['attack'] + UNIT_STATS[unit_type]['defense']) / 2
                total_power += unit_power * count
        return int(total_power)

class ElectricGameDatabase:
    """Game database with Electric-SQL integration"""
    
    def __init__(self):
        self.electric_bridge = electric_bridge
    
    def create_empire(self, name: str, ruler: str, lat: float, lng: float) -> str:
        """Create a new empire with Electric-SQL sync"""
        return self.electric_bridge.create_empire(name, ruler, lat, lng)
    
    def get_empire(self, empire_id: str) -> Optional[Empire]:
        """Get empire with real-time data"""
        empire_data = self.electric_bridge.get_empire(empire_id)
        if empire_data:
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
                created_at=empire_data.get('created_at'),
                updated_at=empire_data.get('updated_at')
            )
            
            # Update resources based on time
            empire.update_resources()
            
            # Save updated resources back to Electric-SQL
            if empire.last_update != empire_data['last_update']:
                self.update_empire(empire)
            
            return empire
        return None
    
    def update_empire(self, empire: Empire) -> bool:
        """Update empire with Electric-SQL sync"""
        updates = {
            'land': empire.land,
            'resources': empire.resources,
            'military': empire.military,
            'location': empire.location,
            'last_update': empire.last_update,
            'cities': empire.cities,
            'buildings': empire.buildings
        }
        
        return self.electric_bridge.update_empire(empire.id, updates)
    
    def get_all_empires(self) -> List[Empire]:
        """Get all empires with real-time data"""
        empires_data = self.electric_bridge.get_all_empires()
        empires = []
        
        for empire_data in empires_data:
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
                created_at=empire_data.get('created_at'),
                updated_at=empire_data.get('updated_at')
            )
            empires.append(empire)
        
        return empires
    
    def build_city(self, empire: Empire, city_type: str, city_name: str) -> bool:
        """Build a city with Electric-SQL sync"""
        if city_type not in CITY_COSTS:
            return False
        
        cost = CITY_COSTS[city_type]
        
        # Check if empire has enough resources
        if (empire.resources.get('gold', 0) >= cost['gold'] and
            empire.resources.get('population', 0) >= cost['population'] and
            empire.land >= cost['land']):
            
            # Deduct resources
            empire.resources['gold'] -= cost['gold']
            empire.resources['population'] -= cost['population']
            empire.land -= cost['land']
            
            # Add city
            city_id = str(uuid.uuid4())
            empire.cities[city_id] = {
                'name': city_name,
                'type': city_type,
                'buildings': {building_type: 0 for building_type in BUILDING_TYPES.keys()},
                'created_at': datetime.now().isoformat()
            }
            
            # Update empire
            self.update_empire(empire)
            
            # Log city creation
            self.electric_bridge.log_game_event(empire.id, 'city_built', {
                'city_name': city_name,
                'city_type': city_type,
                'city_id': city_id
            })
            
            return True
        
        return False
    
    def build_building(self, empire: Empire, city_id: str, building_type: str) -> bool:
        """Build a building with Electric-SQL sync"""
        if city_id not in empire.cities or building_type not in BUILDING_TYPES:
            return False
        
        building_config = BUILDING_TYPES[building_type]
        city = empire.cities[city_id]
        
        # Check building limits
        current_buildings = sum(city['buildings'].values())
        city_type = city['type']
        max_buildings = CITY_STATS[city_type]['max_buildings']
        
        if current_buildings >= max_buildings:
            return False
        
        # Check per-building-type limit
        if city['buildings'][building_type] >= building_config['max_per_city']:
            return False
        
        # Check resources and land
        cost = building_config['cost']
        land_required = building_config['land_required']
        
        if (empire.resources.get('gold', 0) >= cost.get('gold', 0) and
            empire.resources.get('iron', 0) >= cost.get('iron', 0) and
            empire.resources.get('population', 0) >= cost.get('population', 0) and
            empire.land >= land_required):
            
            # Deduct resources
            for resource, amount in cost.items():
                empire.resources[resource] -= amount
            empire.land -= land_required
            
            # Add building
            city['buildings'][building_type] += 1
            empire.buildings[building_type] += 1
            
            # Update empire
            self.update_empire(empire)
            
            # Log building construction
            self.electric_bridge.log_game_event(empire.id, 'building_built', {
                'building_type': building_type,
                'city_id': city_id,
                'city_name': city['name']
            })
            
            return True
        
        return False
    
    def create_battle(self, attacker: Empire, defender: Empire, attacking_units: Dict) -> str:
        """Create a battle with Electric-SQL sync"""
        return self.electric_bridge.create_battle(attacker.id, defender.id, attacking_units)
    
    def send_message(self, from_empire_id: str, to_empire_id: str, message: str, message_type: str = 'general') -> str:
        """Send a message with Electric-SQL sync"""
        return self.electric_bridge.send_message(from_empire_id, to_empire_id, message, message_type)
    
    def get_recent_events(self, empire_id: str = None, limit: int = 50) -> List[Dict]:
        """Get recent game events"""
        return self.electric_bridge.get_recent_events(empire_id, limit)

class BattleSystem:
    """Enhanced battle system with Electric-SQL integration"""
    
    def __init__(self):
        self.electric_bridge = electric_bridge
    
    def execute_battle(self, attacker: Empire, defender: Empire, attacking_units: Dict) -> Dict:
        """Execute battle with real-time updates"""
        
        # Create battle record
        battle_id = self.electric_bridge.create_battle(attacker.id, defender.id, attacking_units)
        
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
        
        # Complete battle in Electric-SQL
        self.electric_bridge.complete_battle(battle_id, result)
        
        # Log battle events
        self.electric_bridge.log_game_event(attacker.id, 'battle_completed', {
            'battle_id': battle_id,
            'result': 'victory' if attacker_wins else 'defeat',
            'defender_id': defender.id
        })
        
        self.electric_bridge.log_game_event(defender.id, 'battle_completed', {
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
electric_db = ElectricGameDatabase()
electric_battle_system = BattleSystem()