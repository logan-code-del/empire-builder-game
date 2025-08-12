#!/usr/bin/env python3
"""
Electric-SQL Setup Script for Empire Builder
Installs and configures Electric-SQL for real-time database synchronization
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_node_npm():
    """Check if Node.js and npm are installed"""
    print("🔍 Checking Node.js and npm installation...")
    
    try:
        node_result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        npm_result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        
        print(f"✅ Node.js version: {node_result.stdout.strip()}")
        print(f"✅ npm version: {npm_result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Node.js or npm not found. Please install Node.js first.")
        print("📥 Download from: https://nodejs.org/")
        return False

def install_electric_sql():
    """Install Electric-SQL dependencies"""
    print("📦 Installing Electric-SQL dependencies...")
    
    # Install npm dependencies
    if not run_command('npm install', 'Installing npm packages'):
        return False
    
    print("✅ Electric-SQL dependencies installed successfully")
    return True

def initialize_electric_database():
    """Initialize Electric-SQL database schema"""
    print("🗄️ Initializing Electric-SQL database schema...")
    
    try:
        # Import the electric bridge to initialize schema
        from electric_bridge import initialize_electric_sql
        
        success = initialize_electric_sql()
        if success:
            print("✅ Electric-SQL database schema initialized")
            return True
        else:
            print("⚠️ Electric-SQL initialized in fallback mode")
            return True
    except Exception as e:
        print(f"❌ Failed to initialize Electric-SQL database: {e}")
        return False

def create_electric_config():
    """Create Electric-SQL configuration files"""
    print("⚙️ Creating Electric-SQL configuration...")
    
    # Create electric.config.json
    config = {
        "app": "empire-builder",
        "migrations": "./migrations",
        "output": "./generated",
        "watch": True,
        "debug": True
    }
    
    try:
        with open('electric.config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Electric-SQL configuration created")
        return True
    except Exception as e:
        print(f"❌ Failed to create Electric-SQL configuration: {e}")
        return False

def test_electric_sql():
    """Test Electric-SQL integration"""
    print("🧪 Testing Electric-SQL integration...")
    
    try:
        from electric_bridge import ElectricSQLBridge
        
        bridge = ElectricSQLBridge()
        bridge.initialize_schema()
        
        print("✅ Electric-SQL integration test passed")
        return True
    except Exception as e:
        print(f"❌ Electric-SQL integration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Empire Builder Electric-SQL Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_node_npm():
        print("\n❌ Setup failed: Node.js/npm not available")
        sys.exit(1)
    
    # Install Electric-SQL
    if not install_electric_sql():
        print("\n❌ Setup failed: Could not install Electric-SQL")
        sys.exit(1)
    
    # Create configuration
    if not create_electric_config():
        print("\n❌ Setup failed: Could not create configuration")
        sys.exit(1)
    
    # Initialize database
    if not initialize_electric_database():
        print("\n❌ Setup failed: Could not initialize database")
        sys.exit(1)
    
    # Test integration
    if not test_electric_sql():
        print("\n⚠️ Setup completed with warnings: Integration test failed")
    else:
        print("\n🎉 Electric-SQL setup completed successfully!")
    
    print("\n📋 Next steps:")
    print("1. Start Electric-SQL server: node electric-client.js")
    print("2. Run the enhanced app: python app_electric.py")
    print("3. Enjoy real-time multiplayer empire building!")
    
    print("\n🔌 Electric-SQL Features Enabled:")
    print("✅ Real-time empire synchronization")
    print("✅ Live battle updates")
    print("✅ Instant messaging")
    print("✅ Real-time resource tracking")
    print("✅ Live game events")
    print("✅ Multiplayer synchronization")

if __name__ == '__main__':
    main()