"""
Supabase Configuration for Empire Builder
Real-time database with PostgreSQL backend
"""

import os
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

class SupabaseConfig:
    """Supabase configuration and client management"""
    
    def __init__(self):
        # Supabase credentials (you'll need to set these)
        self.url = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
        self.key = os.getenv('SUPABASE_ANON_KEY', 'your-anon-key-here')
        self.service_key = os.getenv('SUPABASE_SERVICE_KEY', 'your-service-key-here')
        
        # Initialize client
        self.client: Client = None
        self.is_connected = False
        
    def initialize(self) -> bool:
        """Initialize Supabase client"""
        try:
            self.client = create_client(self.url, self.key)
            
            # Test connection
            response = self.client.table('empires').select('count').execute()
            self.is_connected = True
            print("✅ Supabase connected successfully")
            return True
            
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
            print("⚠️ Using fallback SQLite mode")
            self.is_connected = False
            return False
    
    def get_client(self) -> Client:
        """Get Supabase client"""
        if not self.is_connected:
            self.initialize()
        return self.client

# Global Supabase configuration
supabase_config = SupabaseConfig()

def get_supabase_client() -> Client:
    """Get configured Supabase client"""
    return supabase_config.get_client()

def initialize_supabase() -> bool:
    """Initialize Supabase connection"""
    return supabase_config.initialize()