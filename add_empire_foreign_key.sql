-- Empire Builder - Add Foreign Key Constraint for Empire ID
-- Run this AFTER you've confirmed the empires table exists and has the correct structure

-- Step 1: Check if empires table exists
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'empires') THEN
        RAISE NOTICE 'Empires table found - proceeding with foreign key constraint';
    ELSE
        RAISE EXCEPTION 'Empires table not found! Please create the empires table first.';
    END IF;
END $$;

-- Step 2: Check the structure of the empires table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'empires' AND column_name = 'id';

-- Step 3: Add foreign key constraint (only run if empires table exists and has TEXT id)
-- Uncomment the line below after confirming empires table structure:
-- ALTER TABLE users ADD CONSTRAINT fk_users_empire_id FOREIGN KEY (empire_id) REFERENCES empires(id) ON DELETE SET NULL;

-- Step 4: Verify the constraint was added
-- SELECT constraint_name, table_name, column_name, foreign_table_name, foreign_column_name
-- FROM information_schema.key_column_usage 
-- WHERE table_name = 'users' AND column_name = 'empire_id';

COMMENT ON CONSTRAINT fk_users_empire_id ON users IS 'Links user accounts to their empires';