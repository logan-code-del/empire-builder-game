"""
Supabase Configuration for Empire Builder
Real-time database with PostgreSQL backend
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

# Load environment variables from .env file (override system env vars)
load_dotenv(override=True)

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
            # Check if we have valid credentials
            if (self.url == 'https://your-project.supabase.co' or 
                self.key == 'your-anon-key-here' or
                not self.url or not self.key):
                print("⚠️  Supabase credentials not configured properly")
                print(f"URL: {self.url[:50]}...")
                print(f"Key: {'*' * 20}...")
                print("Using fallback SQLite mode")
                self.is_connected = False
                return False
            
            print(f"🔗 Connecting to Supabase: {self.url}")
            self.client = create_client(self.url, self.key)
            
            # Test connection with a simple query
            print("🧪 Testing Supabase connection...")
            response = self.client.table('empires').select('count').limit(1).execute()
            self.is_connected = True
            print("✅ Supabase connected successfully")
            return True
            
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
            print("🔄 Using fallback SQLite mode")
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

def get_supabase_service_client() -> Client:
    """Get Supabase client with service role key for admin operations"""
    try:
        url = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
        service_key = os.getenv('SUPABASE_SERVICE_KEY', 'your-service-key-here')
        return create_client(url, service_key)
    except Exception as e:
        print(f"Failed to create service client: {e}")
        return None

def initialize_supabase() -> bool:
    """Initialize Supabase connection"""
    return supabase_config.initialize()