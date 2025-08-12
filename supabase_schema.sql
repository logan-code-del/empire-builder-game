-- Supabase Schema for Empire Builder
-- Real-time PostgreSQL database with Row Level Security

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Empires table - core game entities
CREATE TABLE IF NOT EXISTS empires (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    ruler TEXT NOT NULL,
    land INTEGER DEFAULT 2000,
    resources JSONB DEFAULT '{"gold": 10000, "food": 5000, "iron": 2000, "oil": 1000, "population": 1000}',
    military JSONB DEFAULT '{"infantry": 100, "tanks": 10, "aircraft": 5, "ships": 8}',
    location JSONB DEFAULT '{"lat": 0, "lng": 0}',
    last_update TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_ai BOOLEAN DEFAULT FALSE,
    cities JSONB DEFAULT '{}',
    buildings JSONB DEFAULT '{"farm": 0, "mine": 0, "oil_well": 0, "bank": 0, "factory": 0, "barracks": 0, "research_lab": 0, "hospital": 0}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Battles table - real-time battle tracking
CREATE TABLE IF NOT EXISTS battles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    attacker_id UUID NOT NULL REFERENCES empires(id) ON DELETE CASCADE,
    defender_id UUID NOT NULL REFERENCES empires(id) ON DELETE CASCADE,
    attacking_units JSONB NOT NULL,
    defending_units JSONB NOT NULL,
    result JSONB,
    casualties JSONB,
    resources_gained JSONB,
    land_gained INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Messages table - real-time communication
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_empire UUID REFERENCES empires(id) ON DELETE CASCADE,
    to_empire UUID REFERENCES empires(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    message_type TEXT DEFAULT 'general' CHECK (message_type IN ('general', 'alliance', 'trade', 'battle', 'system')),
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Game events table - real-time activity feed
CREATE TABLE IF NOT EXISTS game_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empire_id UUID REFERENCES empires(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resource transactions - real-time resource tracking
CREATE TABLE IF NOT EXISTS resource_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empire_id UUID NOT NULL REFERENCES empires(id) ON DELETE CASCADE,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('production', 'consumption', 'trade', 'battle', 'building')),
    resources JSONB NOT NULL,
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User empire mapping (for authentication integration)
CREATE TABLE IF NOT EXISTS user_empires (
    user_id TEXT NOT NULL,
    empire_id UUID NOT NULL REFERENCES empires(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (user_id, empire_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_empires_name ON empires(name);
CREATE INDEX IF NOT EXISTS idx_empires_created_at ON empires(created_at);
CREATE INDEX IF NOT EXISTS idx_battles_attacker ON battles(attacker_id);
CREATE INDEX IF NOT EXISTS idx_battles_defender ON battles(defender_id);
CREATE INDEX IF NOT EXISTS idx_battles_status ON battles(status);
CREATE INDEX IF NOT EXISTS idx_messages_to_empire ON messages(to_empire);
CREATE INDEX IF NOT EXISTS idx_messages_from_empire ON messages(from_empire);
CREATE INDEX IF NOT EXISTS idx_messages_read ON messages(read);
CREATE INDEX IF NOT EXISTS idx_game_events_empire ON game_events(empire_id);
CREATE INDEX IF NOT EXISTS idx_game_events_type ON game_events(event_type);
CREATE INDEX IF NOT EXISTS idx_resource_transactions_empire ON resource_transactions(empire_id);
CREATE INDEX IF NOT EXISTS idx_user_empires_user ON user_empires(user_id);

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_empires_updated_at 
    BEFORE UPDATE ON empires 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE empires ENABLE ROW LEVEL SECURITY;
ALTER TABLE battles ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE resource_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_empires ENABLE ROW LEVEL SECURITY;

-- RLS Policies for empires (users can only see/edit their own empires)
CREATE POLICY "Users can view all empires" ON empires FOR SELECT USING (true);
CREATE POLICY "Users can insert their own empires" ON empires FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update their own empires" ON empires FOR UPDATE USING (true);

-- RLS Policies for battles (users can see battles involving their empires)
CREATE POLICY "Users can view battles involving their empires" ON battles FOR SELECT USING (true);
CREATE POLICY "Users can create battles with their empires" ON battles FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update battles involving their empires" ON battles FOR UPDATE USING (true);

-- RLS Policies for messages (users can see their own messages)
CREATE POLICY "Users can view their messages" ON messages FOR SELECT USING (true);
CREATE POLICY "Users can send messages" ON messages FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can update their received messages" ON messages FOR UPDATE USING (true);

-- RLS Policies for game events (users can see events for their empires)
CREATE POLICY "Users can view their empire events" ON game_events FOR SELECT USING (true);
CREATE POLICY "System can insert events" ON game_events FOR INSERT WITH CHECK (true);

-- RLS Policies for resource transactions (users can see their own transactions)
CREATE POLICY "Users can view their transactions" ON resource_transactions FOR SELECT USING (true);
CREATE POLICY "System can insert transactions" ON resource_transactions FOR INSERT WITH CHECK (true);

-- RLS Policies for user_empires mapping
CREATE POLICY "Users can view their empire mappings" ON user_empires FOR SELECT USING (true);
CREATE POLICY "System can manage empire mappings" ON user_empires FOR ALL USING (true);

-- Real-time subscriptions setup
-- Enable real-time for all tables
ALTER PUBLICATION supabase_realtime ADD TABLE empires;
ALTER PUBLICATION supabase_realtime ADD TABLE battles;
ALTER PUBLICATION supabase_realtime ADD TABLE messages;
ALTER PUBLICATION supabase_realtime ADD TABLE game_events;
ALTER PUBLICATION supabase_realtime ADD TABLE resource_transactions;

-- Views for easier querying
CREATE OR REPLACE VIEW empire_summary AS
SELECT 
    e.id,
    e.name,
    e.ruler,
    e.land,
    e.resources,
    e.military,
    e.location,
    e.is_ai,
    e.created_at,
    e.updated_at,
    COUNT(DISTINCT b1.id) as battles_won,
    COUNT(DISTINCT b2.id) as battles_lost,
    COUNT(DISTINCT m.id) as unread_messages
FROM empires e
LEFT JOIN battles b1 ON e.id = b1.attacker_id AND (b1.result->>'winner')::UUID = e.id
LEFT JOIN battles b2 ON e.id = b2.defender_id AND (b2.result->>'winner')::UUID != e.id
LEFT JOIN messages m ON e.id = m.to_empire AND m.read = false
GROUP BY e.id, e.name, e.ruler, e.land, e.resources, e.military, e.location, e.is_ai, e.created_at, e.updated_at;

-- Function to calculate empire power
CREATE OR REPLACE FUNCTION calculate_empire_power(empire_military JSONB)
RETURNS INTEGER AS $$
DECLARE
    power INTEGER := 0;
    unit_stats JSONB := '{
        "infantry": {"attack": 10, "defense": 15},
        "tanks": {"attack": 25, "defense": 20},
        "aircraft": {"attack": 30, "defense": 10},
        "ships": {"attack": 20, "defense": 25}
    }';
    unit_type TEXT;
    unit_count INTEGER;
    unit_power INTEGER;
BEGIN
    FOR unit_type IN SELECT jsonb_object_keys(empire_military)
    LOOP
        unit_count := (empire_military->>unit_type)::INTEGER;
        IF unit_stats ? unit_type THEN
            unit_power := ((unit_stats->unit_type->>'attack')::INTEGER + 
                          (unit_stats->unit_type->>'defense')::INTEGER) / 2;
            power := power + (unit_count * unit_power);
        END IF;
    END LOOP;
    
    RETURN power;
END;
$$ LANGUAGE plpgsql;

-- Function to update empire resources based on buildings
CREATE OR REPLACE FUNCTION update_empire_resources(empire_id UUID)
RETURNS VOID AS $$
DECLARE
    empire_record RECORD;
    hours_passed NUMERIC;
    building_production JSONB := '{"gold": 0, "food": 0, "iron": 0, "oil": 0, "population": 0}';
    building_type TEXT;
    building_count INTEGER;
    base_production JSONB := '{"gold": 100, "food": 50, "iron": 25, "oil": 15, "population": 5}';
    building_configs JSONB := '{
        "farm": {"production": {"food": 25}},
        "mine": {"production": {"iron": 15}},
        "oil_well": {"production": {"oil": 10}},
        "bank": {"production": {"gold": 50}},
        "factory": {"production": {"population": 10}},
        "hospital": {"production": {"population": 15}}
    }';
    resource_type TEXT;
    production_amount INTEGER;
BEGIN
    -- Get empire data
    SELECT * INTO empire_record FROM empires WHERE id = empire_id;
    
    -- Calculate hours passed since last update
    hours_passed := EXTRACT(EPOCH FROM (NOW() - empire_record.last_update)) / 3600;
    
    -- Only update if more than 6 minutes have passed
    IF hours_passed < 0.1 THEN
        RETURN;
    END IF;
    
    -- Calculate building production
    FOR building_type IN SELECT jsonb_object_keys(empire_record.buildings)
    LOOP
        building_count := (empire_record.buildings->>building_type)::INTEGER;
        IF building_count > 0 AND building_configs ? building_type THEN
            FOR resource_type IN SELECT jsonb_object_keys(building_configs->building_type->'production')
            LOOP
                production_amount := (building_configs->building_type->'production'->>resource_type)::INTEGER;
                building_production := jsonb_set(
                    building_production,
                    ARRAY[resource_type],
                    ((building_production->>resource_type)::INTEGER + (production_amount * building_count))::TEXT::JSONB
                );
            END LOOP;
        END IF;
    END LOOP;
    
    -- Update empire resources
    UPDATE empires SET
        resources = jsonb_set(
            jsonb_set(
                jsonb_set(
                    jsonb_set(
                        jsonb_set(
                            resources,
                            '{gold}',
                            (GREATEST(0, (resources->>'gold')::INTEGER + 
                                ((base_production->>'gold')::INTEGER + (building_production->>'gold')::INTEGER) * hours_passed))::TEXT::JSONB
                        ),
                        '{food}',
                        (GREATEST(0, (resources->>'food')::INTEGER + 
                            ((base_production->>'food')::INTEGER + (building_production->>'food')::INTEGER) * hours_passed))::TEXT::JSONB
                    ),
                    '{iron}',
                    (GREATEST(0, (resources->>'iron')::INTEGER + 
                        ((base_production->>'iron')::INTEGER + (building_production->>'iron')::INTEGER) * hours_passed))::TEXT::JSONB
                ),
                '{oil}',
                (GREATEST(0, (resources->>'oil')::INTEGER + 
                    ((base_production->>'oil')::INTEGER + (building_production->>'oil')::INTEGER) * hours_passed))::TEXT::JSONB
            ),
            '{population}',
            (GREATEST(0, (resources->>'population')::INTEGER + 
                ((base_production->>'population')::INTEGER + (building_production->>'population')::INTEGER) * hours_passed))::TEXT::JSONB
        ),
        last_update = NOW()
    WHERE id = empire_id;
    
    -- Log resource transaction
    INSERT INTO resource_transactions (empire_id, transaction_type, resources, reason)
    VALUES (
        empire_id,
        'production',
        building_production,
        'Hourly production over ' || ROUND(hours_passed, 1) || ' hours'
    );
END;
$$ LANGUAGE plpgsql;