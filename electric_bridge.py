"""
Electric-SQL Bridge for Empire Builder
Provides Python interface to Electric-SQL real-time database
"""

import json
import subprocess
import threading
import time
import uuid
from typing import Dict, List, Optional, Any
import sqlite3
import os
from datetime import datetime

class ElectricSQLBridge:
    """Bridge between Python Flask app and Electric-SQL client"""
    
    def __init__(self):
        self.electric_process = None
        self.is_running = False
        self.local_db_path = 'empire_electric.db'
        self.fallback_db_path = 'empire_game.db'
        
    def start_electric_client(self):
        """Start the Electric-SQL client process"""
        try:
            # Check if Node.js and npm are available
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            
            # Install dependencies if needed
            if not os.path.exists('node_modules'):
                print("📦 Installing Electric-SQL dependencies...")
                subprocess.run(['npm', 'install'], check=True)
            
            # Start Electric-SQL client
            print("🔌 Starting Electric-SQL client...")
            self.electric_process = subprocess.Popen(
                ['node', 'electric-client.js'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give it time to initialize
            time.sleep(3)
            
            if self.electric_process.poll() is None:
                self.is_running = True
                print("✅ Electric-SQL client started successfully")
                return True
            else:
                print("❌ Electric-SQL client failed to start")
                return False
                
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"⚠️ Electric-SQL not available, using fallback: {e}")
            return False
    
    def stop_electric_client(self):
        """Stop the Electric-SQL client process"""
        if self.electric_process:
            self.electric_process.terminate()
            self.electric_process.wait()
            self.is_running = False
            print("🛑 Electric-SQL client stopped")
    
    def get_connection(self):
        """Get database connection (Electric-SQL or fallback)"""
        if self.is_running and os.path.exists(self.local_db_path):
            return sqlite3.connect(self.local_db_path)
        else:
            return sqlite3.connect(self.fallback_db_path)
    
    def create_empire(self, name: str, ruler: str, lat: float, lng: float) -> str:
        """Create a new empire with Electric-SQL sync"""
        empire_id = str(uuid.uuid4())
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create empire with Electric-SQL compatible structure
        cursor.execute('''
            INSERT INTO empires (
                id, name, ruler, land, resources, military, location, 
                last_update, is_ai, cities, buildings, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            empire_id, name, ruler, 2000,
            json.dumps({'gold': 10000, 'food': 5000, 'iron': 2000, 'oil': 1000, 'population': 1000}),
            json.dumps({'infantry': 100, 'tanks': 10, 'aircraft': 5, 'ships': 8}),
            json.dumps({'lat': lat, 'lng': lng}),
            datetime.now().isoformat(),
            False,
            json.dumps({}),
            json.dumps({
                'farm': 0, 'mine': 0, 'oil_well': 0, 'bank': 0, 
                'factory': 0, 'barracks': 0, 'research_lab': 0, 'hospital': 0
            }),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Log empire creation event
        self.log_game_event(empire_id, 'empire_created', {
            'empire_name': name,
            'ruler': ruler,
            'location': {'lat': lat, 'lng': lng}
        })
        
        print(f"🏰 Empire created with Electric-SQL: {name}")
        return empire_id
    
    def get_empire(self, empire_id: str) -> Optional[Dict]:
        """Get empire data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM empires WHERE id = ?', (empire_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            empire_data = dict(zip(columns, row))
            
            # Parse JSON fields
            empire_data['resources'] = json.loads(empire_data['resources'])
            empire_data['military'] = json.loads(empire_data['military'])
            empire_data['location'] = json.loads(empire_data['location'])
            empire_data['cities'] = json.loads(empire_data['cities'])
            empire_data['buildings'] = json.loads(empire_data['buildings'])
            
            return empire_data
        
        return None
    
    def update_empire(self, empire_id: str, updates: Dict) -> bool:
        """Update empire data with Electric-SQL sync"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Prepare update fields
        set_clauses = []
        values = []
        
        for field, value in updates.items():
            if field in ['resources', 'military', 'cities', 'buildings', 'location']:
                set_clauses.append(f"{field} = ?")
                values.append(json.dumps(value))
            else:
                set_clauses.append(f"{field} = ?")
                values.append(value)
        
        # Always update timestamp
        set_clauses.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(empire_id)
        
        query = f"UPDATE empires SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            print(f"🔄 Empire updated with Electric-SQL: {empire_id}")
        
        return success
    
    def get_all_empires(self) -> List[Dict]:
        """Get all empires"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM empires ORDER BY created_at DESC')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        empires = []
        for row in rows:
            empire_data = dict(zip(columns, row))
            
            # Parse JSON fields
            empire_data['resources'] = json.loads(empire_data['resources'])
            empire_data['military'] = json.loads(empire_data['military'])
            empire_data['location'] = json.loads(empire_data['location'])
            empire_data['cities'] = json.loads(empire_data['cities'])
            empire_data['buildings'] = json.loads(empire_data['buildings'])
            
            empires.append(empire_data)
        
        return empires
    
    def create_battle(self, attacker_id: str, defender_id: str, attacking_units: Dict) -> str:
        """Create a battle with Electric-SQL sync"""
        battle_id = str(uuid.uuid4())
        
        # Get defender's units for battle calculation
        defender = self.get_empire(defender_id)
        defending_units = defender['military'] if defender else {}
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO battles (
                id, attacker_id, defender_id, attacking_units, 
                defending_units, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            battle_id, attacker_id, defender_id,
            json.dumps(attacking_units),
            json.dumps(defending_units),
            'active',
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        # Log battle event
        self.log_game_event(attacker_id, 'battle_started', {
            'defender_id': defender_id,
            'battle_id': battle_id,
            'attacking_units': attacking_units
        })
        
        print(f"⚔️ Battle created with Electric-SQL: {battle_id}")
        return battle_id
    
    def complete_battle(self, battle_id: str, result: Dict) -> bool:
        """Complete a battle with results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE battles SET 
                result = ?, casualties = ?, resources_gained = ?, 
                land_gained = ?, status = ?, completed_at = ?
            WHERE id = ?
        ''', (
            json.dumps(result.get('outcome', {})),
            json.dumps(result.get('casualties', {})),
            json.dumps(result.get('resources_gained', {})),
            result.get('land_gained', 0),
            'completed',
            datetime.now().isoformat(),
            battle_id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        if success:
            print(f"🏆 Battle completed with Electric-SQL: {battle_id}")
        
        return success
    
    def send_message(self, from_empire: str, to_empire: str, message: str, message_type: str = 'general') -> str:
        """Send a message between empires"""
        message_id = f"msg_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (
                id, from_empire, to_empire, message, 
                message_type, read, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            message_id, from_empire, to_empire, message,
            message_type, False, datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        print(f"💬 Message sent with Electric-SQL: {from_empire} -> {to_empire}")
        return message_id
    
    def log_game_event(self, empire_id: str, event_type: str, event_data: Dict) -> str:
        """Log a game event"""
        event_id = f"event_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO game_events (
                id, empire_id, event_type, event_data, created_at
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            event_id, empire_id, event_type,
            json.dumps(event_data), datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return event_id
    
    def log_resource_transaction(self, empire_id: str, transaction_type: str, resources: Dict, reason: str) -> str:
        """Log a resource transaction"""
        transaction_id = f"tx_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resource_transactions (
                id, empire_id, transaction_type, resources, reason, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            transaction_id, empire_id, transaction_type,
            json.dumps(resources), reason, datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return transaction_id
    
    def get_recent_events(self, empire_id: str = None, limit: int = 50) -> List[Dict]:
        """Get recent game events"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if empire_id:
            cursor.execute('''
                SELECT * FROM game_events 
                WHERE empire_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (empire_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM game_events 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        events = []
        for row in rows:
            event_data = dict(zip(columns, row))
            event_data['event_data'] = json.loads(event_data['event_data'])
            events.append(event_data)
        
        return events
    
    def initialize_schema(self):
        """Initialize Electric-SQL compatible schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('electric-schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Execute schema (remove Electric-specific commands for SQLite)
        schema_lines = schema_sql.split('\n')
        clean_schema = []
        
        for line in schema_lines:
            if not line.strip().startswith('ALTER TABLE') or 'ENABLE ELECTRIC' not in line:
                clean_schema.append(line)
        
        cursor.executescript('\n'.join(clean_schema))
        conn.commit()
        conn.close()
        
        print("📋 Electric-SQL schema initialized")

# Global Electric-SQL bridge instance
electric_bridge = ElectricSQLBridge()

def initialize_electric_sql():
    """Initialize Electric-SQL system"""
    try:
        # Initialize schema
        electric_bridge.initialize_schema()
        
        # Try to start Electric-SQL client
        if electric_bridge.start_electric_client():
            print("🚀 Electric-SQL system initialized successfully")
            return True
        else:
            print("⚠️ Electric-SQL client not available, using fallback mode")
            return False
    except Exception as e:
        print(f"❌ Failed to initialize Electric-SQL: {e}")
        return False

def cleanup_electric_sql():
    """Cleanup Electric-SQL system"""
    electric_bridge.stop_electric_client()