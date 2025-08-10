"""
Empire Builder - AI System
Provides AI opponents for single-player gameplay
"""

import random
import time
from typing import List, Dict, Optional
from models import GameDatabase, Empire, BattleSystem, UNIT_COSTS
import threading

class AIPlayer:
    """AI player that makes strategic decisions"""
    
    def __init__(self, empire_id: str, difficulty: str = "normal"):
        self.empire_id = empire_id
        self.difficulty = difficulty
        self.last_action_time = time.time()
        self.strategy = self._determine_strategy()
    
    def _determine_strategy(self) -> str:
        """Determine AI strategy based on difficulty and randomness"""
        strategies = ["aggressive", "defensive", "economic", "balanced"]
        
        if self.difficulty == "easy":
            # Easy AI prefers defensive and economic strategies
            return random.choices(strategies, weights=[1, 3, 3, 2])[0]
        elif self.difficulty == "hard":
            # Hard AI prefers aggressive and balanced strategies
            return random.choices(strategies, weights=[4, 1, 2, 3])[0]
        else:  # normal
            return random.choice(strategies)
    
    def should_take_action(self) -> bool:
        """Determine if AI should take an action based on time and strategy"""
        current_time = time.time()
        time_since_last = current_time - self.last_action_time
        
        # Action frequency based on difficulty
        min_interval = {
            "easy": 120,    # 2 minutes
            "normal": 90,   # 1.5 minutes
            "hard": 60      # 1 minute
        }.get(self.difficulty, 90)
        
        return time_since_last >= min_interval
    
    def make_decision(self, db: GameDatabase, all_empires: List[Empire]) -> Optional[Dict]:
        """Make a strategic decision for the AI"""
        if not self.should_take_action():
            return None
        
        empire = db.get_empire(self.empire_id)
        if not empire:
            return None
        
        self.last_action_time = time.time()
        
        # Decide action based on strategy
        if self.strategy == "aggressive":
            return self._consider_attack(empire, all_empires, db)
        elif self.strategy == "defensive":
            return self._consider_defense(empire, db)
        elif self.strategy == "economic":
            return self._consider_economy(empire, db)
        else:  # balanced
            # Randomly choose between actions
            actions = [
                lambda: self._consider_attack(empire, all_empires, db),
                lambda: self._consider_defense(empire, db),
                lambda: self._consider_economy(empire, db)
            ]
            return random.choice(actions)()
    
    def _consider_attack(self, empire: Empire, all_empires: List[Empire], db: GameDatabase) -> Optional[Dict]:
        """Consider attacking another empire"""
        # Find potential targets (non-AI empires or weaker AI empires)
        targets = []
        
        for target in all_empires:
            if target.id == empire.id:
                continue
            
            # Calculate relative strength
            my_power = self._calculate_military_power(empire.military)
            target_power = self._calculate_military_power(target.military)
            
            # Only attack if we have significant advantage
            if my_power > target_power * 1.2:
                distance = self._calculate_distance(empire.location, target.location)
                targets.append((target, target_power, distance))
        
        if not targets:
            return None
        
        # Choose target (prefer weaker, closer targets)
        targets.sort(key=lambda x: (x[1], x[2]))  # Sort by power, then distance
        target_empire = targets[0][0]
        
        # Decide attack force (use 30-70% of military)
        attack_ratio = random.uniform(0.3, 0.7)
        attacking_units = {}
        
        for unit_type, count in empire.military.items():
            attacking_units[unit_type] = int(count * attack_ratio)
        
        return {
            "action": "attack",
            "target_id": target_empire.id,
            "units": attacking_units
        }
    
    def _consider_defense(self, empire: Empire, db: GameDatabase) -> Optional[Dict]:
        """Consider defensive actions (training units)"""
        # Focus on training defensive units
        available_resources = empire.resources.copy()
        training_plan = {}
        
        # Prioritize infantry and tanks for defense
        unit_priorities = ["infantry", "tanks", "ships", "aircraft"]
        
        for unit_type in unit_priorities:
            if unit_type not in UNIT_COSTS:
                continue
            
            costs = UNIT_COSTS[unit_type]
            max_affordable = float('inf')
            
            for resource, cost in costs.items():
                if cost > 0:
                    max_affordable = min(max_affordable, available_resources.get(resource, 0) // cost)
            
            if max_affordable > 0:
                # Train 20-50% of what we can afford
                train_count = int(max_affordable * random.uniform(0.2, 0.5))
                if train_count > 0:
                    training_plan[unit_type] = train_count
                    
                    # Deduct costs
                    for resource, cost in costs.items():
                        available_resources[resource] -= cost * train_count
        
        if training_plan:
            return {
                "action": "train",
                "units": training_plan
            }
        
        return None
    
    def _consider_economy(self, empire: Empire, db: GameDatabase) -> Optional[Dict]:
        """Consider economic actions (light military training)"""
        # Train small amounts of units to maintain military presence
        available_resources = empire.resources.copy()
        training_plan = {}
        
        # Train small amounts of each unit type
        for unit_type, costs in UNIT_COSTS.items():
            max_affordable = float('inf')
            
            for resource, cost in costs.items():
                if cost > 0:
                    max_affordable = min(max_affordable, available_resources.get(resource, 0) // cost)
            
            if max_affordable > 0:
                # Train only 10-20% of what we can afford
                train_count = int(max_affordable * random.uniform(0.1, 0.2))
                if train_count > 0:
                    training_plan[unit_type] = train_count
                    
                    # Deduct costs
                    for resource, cost in costs.items():
                        available_resources[resource] -= cost * train_count
        
        if training_plan:
            return {
                "action": "train",
                "units": training_plan
            }
        
        return None
    
    def _calculate_military_power(self, military: Dict[str, int]) -> int:
        """Calculate total military power"""
        power = 0
        unit_power = {"infantry": 10, "tanks": 25, "aircraft": 30, "ships": 20}
        
        for unit_type, count in military.items():
            power += count * unit_power.get(unit_type, 0)
        
        return power
    
    def _calculate_distance(self, loc1: Dict, loc2: Dict) -> float:
        """Calculate approximate distance between two locations"""
        lat_diff = loc1.get('lat', 0) - loc2.get('lat', 0)
        lng_diff = loc1.get('lng', 0) - loc2.get('lng', 0)
        return (lat_diff ** 2 + lng_diff ** 2) ** 0.5

class AIManager:
    """Manages all AI players in the game"""
    
    def __init__(self):
        self.ai_players: Dict[str, AIPlayer] = {}
        self.running = False
        self.thread = None
    
    def add_ai_player(self, empire_id: str, difficulty: str = "normal"):
        """Add an AI player"""
        self.ai_players[empire_id] = AIPlayer(empire_id, difficulty)
    
    def remove_ai_player(self, empire_id: str):
        """Remove an AI player"""
        if empire_id in self.ai_players:
            del self.ai_players[empire_id]
    
    def start(self):
        """Start the AI management thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._ai_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Stop the AI management thread"""
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _ai_loop(self):
        """Main AI loop that runs in background"""
        db = GameDatabase()
        
        while self.running:
            try:
                # Get all empires
                all_empires = db.get_all_empires()
                
                # Process each AI player
                for empire_id, ai_player in self.ai_players.items():
                    decision = ai_player.make_decision(db, all_empires)
                    
                    if decision:
                        self._execute_ai_decision(empire_id, decision, db)
                
                # Sleep for a short time before next iteration
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"AI Manager error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _execute_ai_decision(self, empire_id: str, decision: Dict, db: GameDatabase):
        """Execute an AI decision"""
        try:
            empire = db.get_empire(empire_id)
            if not empire:
                return
            
            if decision["action"] == "train":
                # Train units
                units = decision["units"]
                total_cost = {"gold": 0, "iron": 0, "oil": 0, "food": 0}
                
                # Calculate total cost
                for unit_type, count in units.items():
                    if unit_type in UNIT_COSTS:
                        for resource, cost in UNIT_COSTS[unit_type].items():
                            total_cost[resource] += cost * count
                
                # Check if empire can afford it
                can_afford = True
                for resource, cost in total_cost.items():
                    if empire.resources.get(resource, 0) < cost:
                        can_afford = False
                        break
                
                if can_afford:
                    # Deduct resources and add units
                    for resource, cost in total_cost.items():
                        empire.resources[resource] -= cost
                    
                    for unit_type, count in units.items():
                        if unit_type in UNIT_COSTS:
                            empire.military[unit_type] = empire.military.get(unit_type, 0) + count
                    
                    db.update_empire(empire)
                    print(f"AI {empire.name} trained units: {units}")
            
            elif decision["action"] == "attack":
                # Launch attack
                target_id = decision["target_id"]
                attacking_units = decision["units"]
                
                target = db.get_empire(target_id)
                if not target:
                    return
                
                # Validate attacking units
                valid_attack = True
                for unit_type, count in attacking_units.items():
                    if count > empire.military.get(unit_type, 0):
                        valid_attack = False
                        break
                
                if valid_attack:
                    # Calculate battle
                    result = BattleSystem.calculate_battle(empire, target, attacking_units)
                    
                    # Update empires
                    db.update_empire(empire)
                    db.update_empire(target)
                    
                    print(f"AI Battle: {empire.name} vs {target.name} - Winner: {result['winner']}")
        
        except Exception as e:
            print(f"Error executing AI decision: {e}")

def create_ai_empires(db: GameDatabase, count: int = 3) -> List[str]:
    """Create AI empires for single-player mode"""
    ai_empire_ids = []
    
    # Predefined AI empire data
    ai_data = [
        {"name": "Iron Dominion", "ruler": "General Steel", "lat": 55.7558, "lng": 37.6176},  # Moscow
        {"name": "Golden Republic", "ruler": "Emperor Gold", "lat": 39.9042, "lng": 116.4074},  # Beijing
        {"name": "Azure Federation", "ruler": "Admiral Blue", "lat": 51.5074, "lng": -0.1278},  # London
        {"name": "Crimson Empire", "ruler": "Marshal Red", "lat": 48.8566, "lng": 2.3522},  # Paris
        {"name": "Emerald Kingdom", "ruler": "King Green", "lat": 35.6762, "lng": 139.6503},  # Tokyo
    ]
    
    for i in range(min(count, len(ai_data))):
        data = ai_data[i]
        empire_id = db.create_empire(data["name"], data["ruler"], data["lat"], data["lng"])
        
        # Mark as AI empire
        empire = db.get_empire(empire_id)
        empire.is_ai = True
        
        # Give AI empires some extra starting resources and military
        empire.resources["gold"] *= random.randint(2, 4)
        empire.resources["food"] *= random.randint(2, 3)
        empire.resources["iron"] *= random.randint(2, 3)
        empire.resources["oil"] *= random.randint(2, 3)
        
        # Boost military
        for unit_type in empire.military:
            empire.military[unit_type] *= random.randint(2, 5)
        
        db.update_empire(empire)
        ai_empire_ids.append(empire_id)
    
    return ai_empire_ids

# Global AI manager instance
ai_manager = AIManager()

def initialize_ai_system():
    """Initialize the AI system"""
    ai_manager.start()
    return ai_manager