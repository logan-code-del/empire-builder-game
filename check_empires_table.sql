-- Check the structure of the empires table to determine the correct data types
-- Run this in Supabase SQL Editor to see your table structure

-- Check if empires table exists and its structure
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'empires'
ORDER BY ordinal_position;

-- Also check the specific ID column type
SELECT 
    column_name,
    data_type,
    udt_name
FROM information_schema.columns 
WHERE table_name = 'empires' AND column_name = 'id';

-- Show a sample of the empires table to see the actual ID format
SELECT id, name FROM empires LIMIT 3;