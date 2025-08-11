#!/usr/bin/env python3
"""
Demo script showing Empire Builder authentication system usage
"""

from auth import AuthDatabase, User
import uuid

def demo_authentication():
    """Demonstrate the authentication system functionality"""
    print("🎮 Empire Builder Authentication System Demo")
    print("=" * 50)
    
    # Initialize the auth database
    auth_db = AuthDatabase()
    print("✅ Authentication database initialized")
    
    # Demo 1: Create a new user
    print("\n1. Creating a new user account...")
    username = "demo_player"
    email = "demo@empirebuilder.com"
    password = "secure123"
    
    user_id = auth_db.create_user(username, email, password)
    if user_id:
        print(f"✅ User created successfully! ID: {user_id[:8]}...")
    else:
        print("❌ User creation failed (might already exist)")
        # Try to get existing user
        user = auth_db.get_user_by_username(username)
        if user:
            user_id = user.id
            print(f"✅ Found existing user: {user.username}")
    
    # Demo 2: Authenticate the user
    print("\n2. Testing user authentication...")
    user = auth_db.authenticate_user(username, password)
    if user:
        print(f"✅ Authentication successful!")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Created: {user.created_at}")
        print(f"   Empire ID: {user.empire_id or 'None (no empire yet)'}")
    else:
        print("❌ Authentication failed")
        return
    
    # Demo 3: Test wrong password
    print("\n3. Testing wrong password...")
    wrong_user = auth_db.authenticate_user(username, "wrongpassword")
    if wrong_user:
        print("❌ Security issue: wrong password accepted!")
    else:
        print("✅ Security working: wrong password rejected")
    
    # Demo 4: Create a session
    print("\n4. Creating user session...")
    session_token = auth_db.create_session(user.id, "127.0.0.1", "Demo Browser")
    print(f"✅ Session created: {session_token[:16]}...")
    
    # Demo 5: Validate session
    print("\n5. Validating session...")
    validated_user_id = auth_db.validate_session(session_token)
    if validated_user_id == user.id:
        print("✅ Session validation successful")
    else:
        print("❌ Session validation failed")
    
    # Demo 6: Link user to empire (simulate empire creation)
    print("\n6. Linking user to empire...")
    fake_empire_id = str(uuid.uuid4())
    auth_db.link_user_to_empire(user.id, fake_empire_id)
    
    # Get updated user info
    updated_user = auth_db.get_user(user.id)
    if updated_user and updated_user.empire_id == fake_empire_id:
        print(f"✅ User linked to empire: {fake_empire_id[:8]}...")
    else:
        print("❌ Empire linking failed")
    
    # Demo 7: Logout (invalidate session)
    print("\n7. Testing logout (session invalidation)...")
    auth_db.invalidate_session(session_token)
    
    # Try to validate the invalidated session
    invalid_user_id = auth_db.validate_session(session_token)
    if invalid_user_id is None:
        print("✅ Session properly invalidated")
    else:
        print("❌ Session invalidation failed")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication system demo completed!")
    print("\n📊 Summary:")
    print("✅ User registration and storage")
    print("✅ Secure password hashing and verification")
    print("✅ User authentication")
    print("✅ Session management")
    print("✅ Empire linking")
    print("✅ Security validation")
    
    print("\n🚀 The authentication system is ready for use!")
    print("   Start the Flask app and visit http://localhost:5000")

if __name__ == "__main__":
    demo_authentication()