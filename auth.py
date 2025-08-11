"""
Empire Builder - User Authentication System
Handles user registration, login, logout, and session management
"""

import sqlite3
import hashlib
import secrets
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, Dict, Any
from functools import wraps
from flask import session, request, jsonify, redirect, url_for

@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    salt: str
    created_at: str
    last_login: str = None
    is_active: bool = True
    empire_id: str = None

class AuthDatabase:
    def __init__(self):
        self.init_auth_db()
    
    def init_auth_db(self):
        """Initialize authentication database tables"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                is_active BOOLEAN DEFAULT 1,
                empire_id TEXT,
                FOREIGN KEY (empire_id) REFERENCES empires (id)
            )
        ''')
        
        # User sessions table for enhanced security
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Add empire_id column to users table if it doesn't exist (migration)
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN empire_id TEXT')
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use PBKDF2 for secure password hashing
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iterations
        ).hex()
        
        return password_hash, salt
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        test_hash, _ = self.hash_password(password, salt)
        return test_hash == password_hash
    
    def create_user(self, username: str, email: str, password: str) -> Optional[str]:
        """Create a new user account"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect('empire_game.db', timeout=10.0)
                cursor = conn.cursor()
                
                try:
                    # Check if username or email already exists
                    cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
                    if cursor.fetchone():
                        conn.close()
                        return None  # User already exists
                    
                    # Create user
                    user_id = str(uuid.uuid4())
                    password_hash, salt = self.hash_password(password)
                    
                    cursor.execute('''
                        INSERT INTO users (id, username, email, password_hash, salt, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id, username, email, password_hash, salt,
                        datetime.now().isoformat()
                    ))
                    
                    conn.commit()
                    conn.close()
                    return user_id
                    
                except sqlite3.IntegrityError:
                    conn.close()
                    return None
                except Exception as e:
                    conn.close()
                    if attempt == max_retries - 1:
                        raise e
                    continue
                    
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_retries - 1:
                    import time
                    time.sleep(0.1 * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    raise e
        
        return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user login"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, salt, created_at, last_login, is_active, empire_id
            FROM users WHERE username = ? AND is_active = 1
        ''', (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and self.verify_password(password, row[3], row[4]):
            # Update last login
            self.update_last_login(row[0])
            
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                salt=row[4],
                created_at=row[5],
                last_login=row[6],
                is_active=bool(row[7]),
                empire_id=row[8]
            )
        return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, salt, created_at, last_login, is_active, empire_id
            FROM users WHERE id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                salt=row[4],
                created_at=row[5],
                last_login=row[6],
                is_active=bool(row[7]),
                empire_id=row[8]
            )
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, salt, created_at, last_login, is_active, empire_id
            FROM users WHERE username = ?
        ''', (username,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                salt=row[4],
                created_at=row[5],
                last_login=row[6],
                is_active=bool(row[7]),
                empire_id=row[8]
            )
        return None
    
    def update_last_login(self, user_id: str):
        """Update user's last login timestamp"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_login = ? WHERE id = ?
        ''', (datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def link_user_to_empire(self, user_id: str, empire_id: str):
        """Link a user account to an empire"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET empire_id = ? WHERE id = ?
        ''', (empire_id, user_id))
        
        conn.commit()
        conn.close()
    
    def create_session(self, user_id: str, ip_address: str = None, user_agent: str = None) -> str:
        """Create a secure session token"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        session_id = str(uuid.uuid4())
        session_token = secrets.token_urlsafe(32)
        expires_at = (datetime.now() + timedelta(days=30)).isoformat()
        
        cursor.execute('''
            INSERT INTO user_sessions (id, user_id, session_token, created_at, expires_at, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id, user_id, session_token,
            datetime.now().isoformat(), expires_at,
            ip_address, user_agent
        ))
        
        conn.commit()
        conn.close()
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate session token and return user_id"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id FROM user_sessions 
            WHERE session_token = ? AND is_active = 1 AND expires_at > ?
        ''', (session_token, datetime.now().isoformat()))
        
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def invalidate_session(self, session_token: str):
        """Invalidate a session token"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE user_sessions SET is_active = 0 WHERE session_token = ?
        ''', (session_token,))
        
        conn.commit()
        conn.close()
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        conn = sqlite3.connect('empire_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM user_sessions WHERE expires_at < ?
        ''', (datetime.now().isoformat(),))
        
        conn.commit()
        conn.close()

# Global auth database instance
auth_db = AuthDatabase()

def login_required(f):
    """Decorator to require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user() -> Optional[User]:
    """Get the currently logged-in user"""
    if 'user_id' in session:
        return auth_db.get_user(session['user_id'])
    return None

def login_user(user: User, remember_me: bool = False):
    """Log in a user and create session"""
    session['user_id'] = user.id
    session['username'] = user.username
    session['empire_id'] = user.empire_id
    
    if remember_me:
        session.permanent = True
    
    # Create secure session token
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
    user_agent = request.environ.get('HTTP_USER_AGENT', '')
    session_token = auth_db.create_session(user.id, ip_address, user_agent)
    session['session_token'] = session_token

def logout_user():
    """Log out the current user"""
    if 'session_token' in session:
        auth_db.invalidate_session(session['session_token'])
    
    session.clear()