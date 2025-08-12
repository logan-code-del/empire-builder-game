-- Electric-SQL Schema for Empire Builder
-- Real-time synchronized game data

-- Empires table - core game entities
CREATE TABLE IF NOT EXISTS empires (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    ruler TEXT NOT NULL,
    land INTEGER DEFAULT 2000,
    resources TEXT DEFAULT '{"gold": 10000, "food": 5000, "iron": 2000, "oil": 1000, "population": 1000}',
    military TEXT DEFAULT '{"infantry": 100, "tanks": 10, "aircraft": 5, "ships": 8}',
    location TEXT DEFAULT '{"lat": 0, "lng": 0}',
    last_update TEXT DEFAULT CURRENT_TIMESTAMP,
    is_ai BOOLEAN DEFAULT FALSE,
    cities TEXT DEFAULT '{}',
    buildings TEXT DEFAULT '{"farm": 0, "mine": 0, "oil_well": 0, "bank": 0, "factory": 0, "barracks": 0, "research_lab": 0, "hospital": 0}',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Battles table - real-time battle tracking
CREATE TABLE IF NOT EXISTS battles (
    id TEXT PRIMARY KEY,
    attacker_id TEXT NOT NULL,
    defender_id TEXT NOT NULL,
    attacking_units TEXT NOT NULL,
    defending_units TEXT NOT NULL,
    result TEXT,
    casualties TEXT,
    resources_gained TEXT,
    land_gained INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,
    FOREIGN KEY (attacker_id) REFERENCES empires(id),
    FOREIGN KEY (defender_id) REFERENCES empires(id)
);

-- Messages table - real-time communication
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    from_empire TEXT,
    to_empire TEXT,
    message TEXT NOT NULL,
    message_type TEXT DEFAULT 'general',
    read BOOLEAN DEFAULT FALSE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_empire) REFERENCES empires(id),
    FOREIGN KEY (to_empire) REFERENCES empires(id)
);

-- Game events table - real-time activity feed
CREATE TABLE IF NOT EXISTS game_events (
    id TEXT PRIMARY KEY,
    empire_id TEXT,
    event_type TEXT NOT NULL,
    event_data TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empire_id) REFERENCES empires(id)
);

-- Resource transactions - real-time resource tracking
CREATE TABLE IF NOT EXISTS resource_transactions (
    id TEXT PRIMARY KEY,
    empire_id TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    resources TEXT NOT NULL,
    reason TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (empire_id) REFERENCES empires(id)
);

-- Enable Electric-SQL sync for all tables
ALTER TABLE empires ENABLE ELECTRIC;
ALTER TABLE battles ENABLE ELECTRIC;
ALTER TABLE messages ENABLE ELECTRIC;
ALTER TABLE game_events ENABLE ELECTRIC;
ALTER TABLE resource_transactions ENABLE ELECTRIC;