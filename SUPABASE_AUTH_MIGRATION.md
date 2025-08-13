# Supabase Authentication Migration Guide

This guide will help you migrate from SQLite-based authentication to Supabase authentication.

## 🚀 Quick Start

### 1. Set Up Supabase Tables

**First, check your empires table structure:**
1. Go to your Supabase dashboard → SQL Editor
2. Run the contents of `check_empires_table.sql` to see your table structure

**Then, choose the correct schema:**

**Option A: If your empires table uses UUID (recommended):**
1. If you have existing auth tables with wrong types, run `cleanup_auth_tables.sql` first
2. Run `supabase_auth_schema_uuid.sql` to create UUID-compatible tables

**Option B: If your empires table uses TEXT:**
1. Run `supabase_auth_schema_simple.sql` for TEXT-compatible tables

**Most likely you need Option A** since the error indicates UUID/TEXT mismatch.

### 2. Configure Environment Variables

Make sure your `.env` file contains:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here
```

### 3. Test the Setup

Run the setup script to verify everything is working:

```bash
python setup_supabase_auth.py
```

## 📋 What Changed

### Files Modified:
- ✅ `app_supabase.py` - Updated to use Supabase auth
- ✅ Created `auth_supabase.py` - New Supabase authentication module
- ✅ Created `supabase_auth_schema.sql` - Database schema for Supabase

### Authentication Flow:
- **Before**: SQLite database (`empire_game.db`)
- **After**: Supabase PostgreSQL database

## 🔧 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    empire_id UUID REFERENCES empires(id)
);
```

### User Sessions Table
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    ip_address TEXT,
    user_agent TEXT
);
```

## 🔄 Migration Process

### Option 1: Fresh Start (Recommended for Development)
1. Set up Supabase tables using the SQL schema
2. Deploy the updated code
3. Users will need to create new accounts

### Option 2: Data Migration (For Production)
If you have existing users in SQLite, you can migrate them:

1. Export users from SQLite:
```python
import sqlite3
import json

conn = sqlite3.connect('empire_game.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

# Save to JSON for import
with open('users_export.json', 'w') as f:
    json.dump(users, f)
```

2. Import to Supabase using the dashboard or API

## 🛡️ Security Features

### Enhanced Security:
- ✅ **Row Level Security (RLS)** - Users can only access their own data
- ✅ **Session Management** - Secure token-based sessions
- ✅ **Password Hashing** - PBKDF2 with 100,000 iterations
- ✅ **Session Expiration** - Automatic cleanup of expired sessions

### Policies Applied:
- Users can only view/update their own profile
- Users can only manage their own sessions
- Service role has full access for server operations

## 🚨 Important Notes

### Environment Variables:
Make sure these are set in your deployment environment (Render):
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_KEY` (optional, for admin operations)

### Database Permissions:
The service key is used for server-side operations. Make sure it has the necessary permissions in your Supabase project.

### Session Management:
Sessions are now stored in Supabase and will persist across deployments, unlike SQLite which was lost on each deployment.

## 🧪 Testing

### Test Authentication:
1. Register a new user
2. Login with the user
3. Check that the session persists
4. Verify user data is stored in Supabase

### Verify Tables:
```sql
-- Check users table
SELECT COUNT(*) FROM users;

-- Check sessions table  
SELECT COUNT(*) FROM user_sessions;

-- Check active sessions
SELECT COUNT(*) FROM user_sessions WHERE is_active = true;
```

## 🔍 Troubleshooting

### Common Issues:

1. **SQL Type Casting Error (`operator does not exist: text = uuid`)**
   - Use `supabase_auth_schema_simple.sql` instead of the original schema
   - This uses TEXT types consistently to avoid casting issues

2. **Connection Failed**
   - Check SUPABASE_URL and SUPABASE_ANON_KEY
   - Verify Supabase project is active

3. **Table Not Found**
   - Run the SQL schema in Supabase dashboard
   - Check table names match exactly

4. **Foreign Key Constraint Error**
   - The simplified schema doesn't include foreign key constraints initially
   - Add them later using `add_empire_foreign_key.sql` after confirming table structure

5. **Permission Denied**
   - Verify RLS policies are set correctly
   - Check service key permissions

6. **Session Issues**
   - Clear browser cookies/session storage
   - Check session expiration times

### Debug Mode:
Enable debug logging to see detailed error messages:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify your Supabase dashboard for table structure
3. Test the connection using `setup_supabase_auth.py`
4. Check that all environment variables are properly set

## 🎉 Benefits of Supabase Auth

- ✅ **Persistent Data** - No data loss on deployments
- ✅ **Scalability** - PostgreSQL handles concurrent users
- ✅ **Real-time** - Built-in real-time capabilities
- ✅ **Security** - Enterprise-grade security features
- ✅ **Backup** - Automatic backups and point-in-time recovery
- ✅ **Monitoring** - Built-in analytics and monitoring