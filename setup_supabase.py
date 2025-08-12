#!/usr/bin/env python3
"""
Supabase Setup Script for Empire Builder
Configures Supabase for real-time database functionality
"""

import os
import sys
import subprocess
from pathlib import Path

def install_supabase_dependencies():
    """Install Supabase Python dependencies"""
    print("Installing Supabase dependencies...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'supabase==2.3.4', 'postgrest==0.13.2'], 
                      check=True, capture_output=True, text=True)
        print("Supabase dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Supabase dependencies: {e}")
        return False

def create_env_template():
    """Create environment template for Supabase credentials"""
    env_template = """# Supabase Configuration for Empire Builder
# Get these values from your Supabase project dashboard

# Your Supabase project URL
SUPABASE_URL=https://your-project-id.supabase.co

# Your Supabase anon/public key
SUPABASE_ANON_KEY=your-anon-key-here

# Your Supabase service role key (for admin operations)
SUPABASE_SERVICE_KEY=your-service-key-here

# Flask configuration
SECRET_KEY=empire-builder-supabase-secret-key-2024
"""
    
    try:
        with open('.env.template', 'w', encoding='utf-8') as f:
            f.write(env_template)
        
        print("Environment template created (.env.template)")
        print("Copy this to .env and add your Supabase credentials")
        return True
    except Exception as e:
        print(f"Failed to create environment template: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("Testing Supabase integration...")
    
    try:
        from supabase_config import initialize_supabase
        
        # This will test with default/placeholder values
        success = initialize_supabase()
        
        if success:
            print("Supabase integration test passed")
        else:
            print("Supabase not configured - will use SQLite fallback")
        
        return True
    except Exception as e:
        print(f"Supabase integration test failed: {e}")
        return False

def create_supabase_instructions():
    """Create setup instructions for Supabase"""
    instructions = """# Supabase Setup Instructions for Empire Builder

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login to your account
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - Name: `empire-builder`
   - Database Password: (choose a strong password)
   - Region: (choose closest to your users)
6. Click "Create new project"

## 2. Get Your Credentials

Once your project is created:

1. Go to **Settings** -> **API**
2. Copy these values:
   - **Project URL**: `https://your-project-id.supabase.co`
   - **anon/public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
   - **service_role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## 3. Configure Environment

1. Copy `.env.template` to `.env`:
   ```bash
   copy .env.template .env
   ```

2. Edit `.env` with your credentials:
   ```
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-actual-anon-key
   SUPABASE_SERVICE_KEY=your-actual-service-key
   ```

## 4. Set Up Database Schema

1. Go to **SQL Editor** in your Supabase dashboard
2. Copy the contents of `supabase_schema.sql`
3. Paste and run the SQL to create tables and functions

## 5. Enable Real-time

1. Go to **Database** -> **Replication**
2. Enable replication for these tables:
   - `empires`
   - `battles`
   - `messages`
   - `game_events`
   - `resource_transactions`

## 6. Test Your Setup

Run the enhanced app:
```bash
python app_supabase.py
```

Look for this message:
```
Supabase real-time features enabled
```

## 7. Deploy to Production

For Render deployment, add environment variables:
1. Go to your Render dashboard
2. Select your service
3. Go to **Environment**
4. Add:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_KEY`

## You're Ready!

Your Empire Builder now has:
- Real-time database synchronization
- Live multiplayer updates
- Instant battle notifications
- Real-time messaging
- Live resource tracking
- Automatic fallback to SQLite

## Troubleshooting

### Connection Issues
- Check your credentials in `.env`
- Verify your Supabase project is active
- Check network connectivity

### Schema Issues
- Make sure you ran the complete `supabase_schema.sql`
- Check for any SQL errors in Supabase dashboard
- Verify all tables were created

### Real-time Not Working
- Enable replication for all tables
- Check WebSocket connection in browser console
- Verify real-time subscriptions are active

### Fallback Mode
If Supabase is unavailable, the app automatically uses SQLite:
- All features still work
- No data loss
- No real-time sync (single-player mode)

## Support

If you need help:
1. Check the Supabase documentation
2. Verify your setup against this guide
3. Test with the fallback SQLite mode first
"""
    
    try:
        with open('SUPABASE_SETUP.md', 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print("Setup instructions created (SUPABASE_SETUP.md)")
        return True
    except Exception as e:
        print(f"Failed to create setup instructions: {e}")
        return False

def main():
    """Main setup function"""
    print("Empire Builder Supabase Setup")
    print("=" * 50)
    
    # Install dependencies
    if not install_supabase_dependencies():
        print("\nSetup failed: Could not install dependencies")
        sys.exit(1)
    
    # Create environment template
    if not create_env_template():
        print("\nSetup failed: Could not create environment template")
        sys.exit(1)
    
    # Create setup instructions
    if not create_supabase_instructions():
        print("\nSetup failed: Could not create instructions")
        sys.exit(1)
    
    # Test integration
    if not test_supabase_connection():
        print("\nSetup completed with warnings: Integration test failed")
    else:
        print("\nSupabase setup completed successfully!")
    
    print("\nNext steps:")
    print("1. Create a Supabase project at https://supabase.com")
    print("2. Copy .env.template to .env and add your credentials")
    print("3. Run the SQL schema in your Supabase dashboard")
    print("4. Enable real-time replication for all tables")
    print("5. Test with: python app_supabase.py")
    
    print("\nRead SUPABASE_SETUP.md for detailed instructions")
    
    print("\nSupabase Features:")
    print("- Real-time PostgreSQL database")
    print("- Instant multiplayer synchronization")
    print("- Live battle updates and notifications")
    print("- Real-time messaging between players")
    print("- Live resource tracking and events")
    print("- Automatic SQLite fallback")
    print("- Production-ready deployment")

if __name__ == '__main__':
    main()