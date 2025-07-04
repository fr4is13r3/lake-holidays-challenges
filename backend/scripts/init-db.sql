-- Initial database setup for Lake Holidays Challenge
-- This script is run automatically by Docker Compose

-- Create database if it doesn't exist (PostgreSQL)
SELECT 'CREATE DATABASE lake_holidays' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lake_holidays')\gexec

-- Create test database for testing
SELECT 'CREATE DATABASE lake_holidays_test' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'lake_holidays_test')\gexec

-- Create extensions
\c lake_holidays;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "postgis" CASCADE;  -- For geographic data (if needed)

\c lake_holidays_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Switch back to main database
\c lake_holidays;

-- Create initial indexes for performance
-- These will be supplemented by Alembic migrations
