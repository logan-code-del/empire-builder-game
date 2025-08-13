-- Empire Builder - Supabase Authentication Tables (UUID Compatible)
-- This version uses UUID types to match your existing empires table
-- Run these commands in your Supabase SQL editor

-- Step 1: Create users table with UUID types
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    empire_id UUID REFERENCES empires(id) ON DELETE SET NULL
);

-- Step 2: Create user sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    ip_address TEXT,
    user_agent TEXT
);

-- Step 3: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_empire_id ON users(empire_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires ON user_sessions(expires_at);

-- Step 4: Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;

-- Step 5: Create RLS policies for service role access (for server-side operations)
CREATE POLICY "Service role full access users" ON users
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access sessions" ON user_sessions
    FOR ALL USING (auth.role() = 'service_role');

-- Step 6: Create policies for authenticated users (optional - for future client-side access)
-- Note: These policies use UUID casting for compatibility
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own sessions" ON user_sessions
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can manage own sessions" ON user_sessions
    FOR ALL USING (user_id = auth.uid());

-- Step 7: Function to cleanup expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM user_sessions 
    WHERE expires_at < NOW() OR is_active = false;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add comments
COMMENT ON TABLE users IS 'User accounts for Empire Builder game';
COMMENT ON TABLE user_sessions IS 'Active user sessions with security tokens';
COMMENT ON FUNCTION cleanup_expired_sessions() IS 'Removes expired and inactive user sessions';

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Empire Builder authentication tables created successfully with UUID types!';
    RAISE NOTICE 'Tables created: users, user_sessions';
    RAISE NOTICE 'Foreign key constraint to empires table applied';
    RAISE NOTICE 'Indexes and policies applied';
END $$;