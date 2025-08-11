# Empire Builder - User Authentication System

## Overview

The Empire Builder game now includes a comprehensive user authentication system that allows players to create accounts, log in, log out, and securely manage their empires. This system ensures that each player's progress is saved and protected.

## Features

### 🔐 Security Features
- **Password Hashing**: Uses PBKDF2 with SHA-256 and 100,000 iterations
- **Salt Protection**: Each password has a unique salt for maximum security
- **Session Management**: Secure session tokens with expiration
- **CSRF Protection**: Built-in Flask session security
- **Input Validation**: Comprehensive form validation on both client and server side

### 👤 User Management
- **User Registration**: Create new accounts with username, email, and password
- **User Login**: Secure authentication with "Remember Me" option
- **User Logout**: Clean session termination
- **Account Linking**: Each user account is linked to their empire
- **Session Persistence**: Stay logged in for up to 30 days (if "Remember Me" is checked)

### 🎮 Game Integration
- **Empire Ownership**: Each empire is now owned by a specific user account
- **Protected Routes**: All game features require authentication
- **Seamless Experience**: Automatic redirection between login/empire creation
- **Real-time Updates**: Socket.IO integration with user authentication

## How to Use

### For New Players

1. **Visit the Game**: Go to `http://localhost:5000`
2. **Create Account**: Click "Create Account & Empire"
3. **Fill Registration Form**:
   - Choose a unique username (3-20 characters)
   - Enter a valid email address
   - Create a strong password (minimum 6 characters)
   - Confirm your password
   - Agree to terms of service
4. **Complete Registration**: Click "Create My Empire Account"
5. **Login**: You'll be redirected to login with your new credentials
6. **Create Empire**: After login, create your empire and start playing!

### For Returning Players

1. **Visit the Game**: Go to `http://localhost:5000`
2. **Login**: Click "Login" and enter your credentials
3. **Remember Me**: Check the box to stay logged in for 30 days
4. **Play**: Access your existing empire and continue your conquest!

### Logout

- Click on your username in the top navigation
- Select "Logout" from the dropdown menu
- You'll be safely logged out and redirected to the main page

## Technical Implementation

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
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
);
```

#### User Sessions Table
```sql
CREATE TABLE user_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_token TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### API Endpoints

#### Authentication Routes
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

#### Protected Routes
All game routes now require authentication:
- `/dashboard` - Empire dashboard
- `/world_map` - World map view
- `/military` - Military management
- `/cities` - City management
- `/create_empire` - Empire creation
- All `/api/*` endpoints

### Security Measures

1. **Password Security**:
   - PBKDF2 hashing with SHA-256
   - 100,000 iterations for slow hashing
   - Unique salt per password
   - Minimum 6 character requirement

2. **Session Security**:
   - Secure session tokens
   - 30-day expiration with "Remember Me"
   - IP address and user agent tracking
   - Automatic cleanup of expired sessions

3. **Input Validation**:
   - Username: 3-20 characters, alphanumeric + underscore
   - Email: Valid email format required
   - Password: Minimum 6 characters
   - Client-side and server-side validation

4. **Route Protection**:
   - `@login_required` decorator on all protected routes
   - Automatic redirection to login page
   - JSON API error responses for AJAX requests

## File Structure

```
empire/
├── auth.py                 # Authentication system core
├── app.py                  # Main application (updated with auth)
├── templates/
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   └── base.html          # Updated navigation with auth
├── test_auth.py           # Authentication testing script
└── AUTHENTICATION_GUIDE.md # This documentation
```

## Testing

Run the authentication test script:
```bash
cd empire
python test_auth.py
```

This will verify:
- Registration page accessibility
- Login page functionality
- Protected route security
- Main page authentication options

## Troubleshooting

### Common Issues

1. **"Username already exists"**
   - Choose a different username
   - Usernames must be unique across all users

2. **"Invalid username or password"**
   - Check your credentials carefully
   - Passwords are case-sensitive

3. **"Authentication required" errors**
   - You need to log in to access game features
   - Sessions may have expired

4. **Registration form validation errors**
   - Ensure all fields are filled correctly
   - Password must be at least 6 characters
   - Username can only contain letters, numbers, and underscores

### Database Issues

If you encounter database errors:
1. The authentication system automatically creates required tables
2. Existing empires are preserved and can be linked to new user accounts
3. The system handles database migrations automatically

## Migration from Old System

If you have existing empires from before the authentication system:
1. Create a new user account
2. Your existing empire data is preserved in the database
3. Contact an administrator to link your old empire to your new account if needed

## Security Best Practices

1. **Use Strong Passwords**: Minimum 6 characters, include numbers and symbols
2. **Keep Credentials Safe**: Don't share your login information
3. **Log Out**: Always log out when using shared computers
4. **Regular Updates**: Keep your email address current for account recovery

## Future Enhancements

Planned features for future versions:
- Password reset via email
- Two-factor authentication (2FA)
- Account settings page
- Empire transfer between accounts
- Admin panel for user management
- OAuth integration (Google, Discord, etc.)

## Support

If you encounter any issues with the authentication system:
1. Check this guide for common solutions
2. Verify the server is running properly
3. Check browser console for JavaScript errors
4. Ensure cookies are enabled in your browser

---

**Empire Builder Authentication System v1.0**  
*Secure, user-friendly authentication for the ultimate strategy game experience!*