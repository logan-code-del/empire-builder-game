Authentication System
=====================

Empire Builder uses a custom authentication system built on Supabase, providing secure user management, session handling, and role-based access control.

Overview
--------

The authentication system handles:
- User registration and login
- Secure password hashing and verification
- Session management with tokens
- User profile management
- Integration with game data (empires)

Architecture
------------

**Components:**
- **auth_supabase.py**: Core authentication logic
- **Supabase Database**: User data storage with Row Level Security
- **Flask Sessions**: Web session management
- **Environment Configuration**: Secure credential management

**Security Features:**
- PBKDF2 password hashing with salt
- UUID-based user identifiers
- Secure session tokens
- Row Level Security (RLS) policies
- Service role separation

User Registration
-----------------

Registration Process
~~~~~~~~~~~~~~~~~~~~

1. **Form Validation**
   - Username: 3+ characters, unique
   - Email: Valid format, unique
   - Password: 6+ characters minimum
   - Password confirmation match

2. **Security Checks**
   - Username availability check
   - Email format validation
   - Password strength requirements
   - Duplicate prevention

3. **Account Creation**
   - Password hashing with PBKDF2
   - UUID generation for user ID
   - Database record creation
   - Success confirmation

**Registration Endpoint:**

.. code-block:: python

   @app.route('/register', methods=['GET', 'POST'])
   def register():
       # Handle both form and JSON requests
       # Validate input data
       # Create user account
       # Return success/error response

**Example Registration Request:**

.. code-block:: javascript

   // JSON API request
   fetch('/register', {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({
           username: 'player123',
           email: 'player@example.com',
           password: 'securepassword',
           confirm_password: 'securepassword'
       })
   })

User Login
----------

Login Process
~~~~~~~~~~~~~

1. **Credential Verification**
   - Username/email lookup
   - Password hash comparison
   - Account status check

2. **Session Creation**
   - Generate secure session token
   - Store session in database
   - Set browser session cookie
   - Update last login timestamp

3. **Redirect to Dashboard**
   - Successful login redirects to game
   - Failed login shows error message

**Login Endpoint:**

.. code-block:: python

   @app.route('/login', methods=['GET', 'POST'])
   def login():
       # Authenticate user credentials
       # Create session if valid
       # Redirect to dashboard

**Example Login Request:**

.. code-block:: javascript

   // Form submission
   <form method="POST" action="/login">
       <input name="username" required>
       <input name="password" type="password" required>
       <input name="remember_me" type="checkbox">
       <button type="submit">Login</button>
   </form>

Password Security
-----------------

Hashing Algorithm
~~~~~~~~~~~~~~~~~

Empire Builder uses PBKDF2 (Password-Based Key Derivation Function 2) for secure password storage:

.. code-block:: python

   def hash_password(self, password: str, salt: str = None) -> tuple:
       """Hash password with salt using PBKDF2"""
       if salt is None:
           salt = secrets.token_hex(32)
       
       password_hash = hashlib.pbkdf2_hmac(
           'sha256',
           password.encode('utf-8'),
           salt.encode('utf-8'),
           100000  # 100,000 iterations
       ).hex()
       
       return password_hash, salt

**Security Properties:**
- **Salt**: Unique random salt per password
- **Iterations**: 100,000 iterations (slow brute force)
- **Algorithm**: SHA-256 based PBKDF2
- **Storage**: Hash and salt stored separately

Password Verification
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
       """Verify password against stored hash"""
       test_hash, _ = self.hash_password(password, salt)
       return test_hash == password_hash

Session Management
------------------

Session Creation
~~~~~~~~~~~~~~~~

When a user logs in successfully:

1. **Generate Token**: Cryptographically secure random token
2. **Store Session**: Save to database with expiration
3. **Set Cookie**: Browser session cookie
4. **Track Metadata**: IP address, user agent, timestamp

.. code-block:: python

   def create_session(self, user_id: str, ip_address: str = None, 
                     user_agent: str = None) -> str:
       """Create a secure session token"""
       session_token = secrets.token_urlsafe(32)
       expires_at = (datetime.now() + timedelta(days=30)).isoformat()
       
       session_data = {
           'user_id': user_id,
           'session_token': session_token,
           'expires_at': expires_at,
           'created_at': datetime.now().isoformat(),
           'ip_address': ip_address,
           'user_agent': user_agent
       }
       
       # Store in database
       result = self.service_client.table('user_sessions').insert(session_data).execute()
       return session_token if result.data else None

Session Validation
~~~~~~~~~~~~~~~~~~

For each authenticated request:

1. **Extract Token**: From session cookie
2. **Database Lookup**: Find active session
3. **Expiration Check**: Verify not expired
4. **User Loading**: Load associated user data

.. code-block:: python

   def get_user_by_session(self, session_token: str) -> Optional[User]:
       """Get user by session token"""
       # Query active session
       # Check expiration
       # Return user object or None

Authentication Decorators
-------------------------

Route Protection
~~~~~~~~~~~~~~~~

The ``@login_required`` decorator protects routes that need authentication:

.. code-block:: python

   def login_required(f):
       """Decorator to require login for routes"""
       @wraps(f)
       def decorated_function(*args, **kwargs):
           current_user = get_current_user()
           if not current_user:
               if request.is_json:
                   return jsonify({'error': 'Authentication required'}), 401
               return redirect(url_for('login'))
           return f(*args, **kwargs)
       return decorated_function

**Usage Example:**

.. code-block:: python

   @app.route('/dashboard')
   @login_required
   def dashboard():
       current_user = get_current_user()
       # Protected route logic
       return render_template('dashboard.html', user=current_user)

User Management
---------------

User Model
~~~~~~~~~~

.. code-block:: python

   @dataclass
   class User:
       id: str              # UUID primary key
       username: str        # Unique username
       email: str          # Unique email address
       password_hash: str   # Hashed password
       salt: str           # Password salt
       created_at: str     # Registration timestamp
       last_login: str     # Last login timestamp
       is_active: bool     # Account status
       empire_id: str      # Linked empire (optional)

User Operations
~~~~~~~~~~~~~~~

**Get Current User:**

.. code-block:: python

   def get_current_user() -> Optional[User]:
       """Get currently logged-in user"""
       session_token = session.get('session_token')
       if session_token:
           return supabase_auth_db.get_user_by_session(session_token)
       return None

**Update User Profile:**

.. code-block:: python

   def update_user_profile(user_id: str, updates: dict):
       """Update user profile information"""
       # Validate updates
       # Apply changes to database
       # Return success/failure

**Link User to Empire:**

.. code-block:: python

   def link_user_to_empire(self, user_id: str, empire_id: str):
       """Link user account to game empire"""
       service_client = self.service_client or self.client
       service_client.table('users').update({
           'empire_id': empire_id
       }).eq('id', user_id).execute()

Database Schema
---------------

Users Table
~~~~~~~~~~~

.. code-block:: sql

   CREATE TABLE users (
       id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       salt VARCHAR(255) NOT NULL,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       last_login TIMESTAMP WITH TIME ZONE,
       is_active BOOLEAN DEFAULT TRUE,
       empire_id UUID REFERENCES empires(id)
   );

User Sessions Table
~~~~~~~~~~~~~~~~~~~

.. code-block:: sql

   CREATE TABLE user_sessions (
       id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
       user_id UUID REFERENCES users(id) ON DELETE CASCADE,
       session_token VARCHAR(255) UNIQUE NOT NULL,
       expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
       ip_address INET,
       user_agent TEXT
   );

Row Level Security
~~~~~~~~~~~~~~~~~~

.. code-block:: sql

   -- Enable RLS on users table
   ALTER TABLE users ENABLE ROW LEVEL SECURITY;

   -- Service role can manage all users
   CREATE POLICY "Service role can manage users" ON users
   FOR ALL USING (auth.role() = 'service_role');

   -- Users can view their own data
   CREATE POLICY "Users can view own data" ON users
   FOR SELECT USING (auth.uid() = id);

Security Considerations
-----------------------

Best Practices
~~~~~~~~~~~~~~

**Password Security:**
- Minimum 6 characters (consider increasing)
- PBKDF2 with 100,000 iterations
- Unique salt per password
- Secure random salt generation

**Session Security:**
- Cryptographically secure tokens
- 30-day expiration (configurable)
- IP and user agent tracking
- Automatic cleanup of expired sessions

**Database Security:**
- Row Level Security enabled
- Service role for admin operations
- Separate anon key for client operations
- Environment variable configuration

**Application Security:**
- Input validation and sanitization
- CSRF protection (Flask-WTF recommended)
- Rate limiting on auth endpoints
- Secure cookie configuration

Common Issues and Solutions
---------------------------

Registration Problems
~~~~~~~~~~~~~~~~~~~~~

**"Row Level Security" Error:**
- Ensure service key is used for user creation
- Verify RLS policies are correctly configured
- Check that service client is initialized

**"Username already exists":**
- Implement proper uniqueness checking
- Provide clear error messages
- Consider case-insensitive usernames

Login Problems
~~~~~~~~~~~~~~

**"Invalid username or password":**
- Check password hashing consistency
- Verify database connection
- Ensure user account is active

**Session Issues:**
- Check session token generation
- Verify database session storage
- Confirm cookie configuration

**Environment Variables:**
- Use ``load_dotenv(override=True)`` to override system vars
- Verify all required variables are set
- Check for typos in variable names

Testing Authentication
----------------------

Debug Scripts
~~~~~~~~~~~~~

The project includes debug scripts for testing:

**Registration Test:**

.. code-block:: bash

   python debug_registration.py

**Login Test:**

.. code-block:: bash

   python debug_login.py

**Connection Test:**

.. code-block:: bash

   python test_simple_connection.py

Manual Testing
~~~~~~~~~~~~~~

1. **Registration Flow:**
   - Try valid registration
   - Test validation errors
   - Verify database records

2. **Login Flow:**
   - Test valid credentials
   - Test invalid credentials
   - Verify session creation

3. **Session Management:**
   - Test protected routes
   - Verify logout functionality
   - Check session expiration

API Integration
---------------

For external applications or mobile clients:

**JSON API Endpoints:**
- ``POST /register``: Create new account
- ``POST /login``: Authenticate user
- ``POST /logout``: End session
- ``GET /api/user/profile``: Get user info

**Authentication Headers:**
- Use session tokens in Authorization header
- Support both cookie and header auth
- Consistent error responses

This authentication system provides a secure, scalable foundation for Empire Builder's user management needs while maintaining flexibility for future enhancements.