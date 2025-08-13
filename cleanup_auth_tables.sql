-- Cleanup script for authentication tables
-- Run this ONLY if you need to start fresh and remove existing auth tables
-- WARNING: This will delete all user data!

-- Drop existing policies first
DROP POLICY IF EXISTS "Users can view own data" ON users;
DROP POLICY IF EXISTS "Users can update own data" ON users;
DROP POLICY IF EXISTS "Users can view own sessions" ON user_sessions;
DROP POLICY IF EXISTS "Users can manage own sessions" ON user_sessions;
DROP POLICY IF EXISTS "Service role full access users" ON users;
DROP POLICY IF EXISTS "Service role full access sessions" ON user_sessions;

-- Drop existing tables (this will delete all data!)
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop function if it exists
DROP FUNCTION IF EXISTS cleanup_expired_sessions();

-- Confirmation message
DO $$
BEGIN
    RAISE NOTICE 'Authentication tables cleaned up successfully!';
    RAISE NOTICE 'You can now run the UUID-compatible schema.';
END $$;