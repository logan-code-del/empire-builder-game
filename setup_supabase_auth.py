"""
Setup script for Supabase Authentication
This script helps set up the authentication tables in Supabase
"""

import os
from supabase_config import get_supabase_client

def setup_supabase_auth():
    """Setup Supabase authentication tables"""
    print("🚀 Setting up Supabase Authentication...")
    
    try:
        client = get_supabase_client()
        
        # Test connection
        print("📡 Testing Supabase connection...")
        test_result = client.table('empires').select('count').limit(1).execute()
        print("✅ Supabase connection successful!")
        
        # Check if auth tables exist
        print("🔍 Checking authentication tables...")
        
        try:
            users_result = client.table('users').select('count').limit(1).execute()
            print("✅ Users table exists")
        except Exception as e:
            print(f"❌ Users table missing: {e}")
            print("📋 Please create the users table using the SQL schema")
        
        try:
            sessions_result = client.table('user_sessions').select('count').limit(1).execute()
            print("✅ User sessions table exists")
        except Exception as e:
            print(f"❌ User sessions table missing: {e}")
            print("📋 Please create the user_sessions table using the SQL schema")
        
        print("\n📝 Setup Instructions:")
        print("1. Go to your Supabase dashboard")
        print("2. Navigate to the SQL Editor")
        print("3. Run the SQL commands from 'supabase_auth_schema.sql'")
        print("4. Make sure your environment variables are set:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_ANON_KEY")
        print("   - SUPABASE_SERVICE_KEY (optional)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up Supabase auth: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your Supabase credentials in .env file")
        print("2. Make sure your Supabase project is active")
        print("3. Verify your internet connection")
        return False

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"✅ {var} is set")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\n📝 Please add these to your .env file:")
        for var in missing_vars:
            print(f"{var}=your_value_here")
        return False
    
    print("✅ All required environment variables are set")
    return True

if __name__ == '__main__':
    print("🎮 Empire Builder - Supabase Authentication Setup")
    print("=" * 50)
    
    # Check environment first
    if not check_environment():
        print("\n❌ Please fix environment variables before continuing")
        exit(1)
    
    # Setup authentication
    if setup_supabase_auth():
        print("\n🎉 Supabase authentication setup completed!")
        print("You can now use Supabase for user authentication")
    else:
        print("\n❌ Setup failed. Please check the errors above")
        exit(1)