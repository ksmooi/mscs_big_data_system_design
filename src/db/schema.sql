-- Schema for StockVision

-- Table: stock_data
-- This table stores raw stock data retrieved from the Yahoo Finance API.
CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,                  -- Unique identifier for each record
    ticker VARCHAR(10) NOT NULL,            -- Stock ticker symbol
    date DATE NOT NULL,                     -- Date of the stock data
    open DECIMAL(10, 2) DEFAULT 0,          -- Opening price of the stock
    high DECIMAL(10, 2) DEFAULT 0,          -- Highest price of the stock
    low DECIMAL(10, 2) DEFAULT 0,           -- Lowest price of the stock
    close DECIMAL(10, 2) DEFAULT 0,         -- Closing price of the stock
    volume BIGINT DEFAULT 0,                -- Trading volume
    UNIQUE (ticker, date)                   -- Ensure no duplicate records for the same ticker and date
);

-- Table: stock_analysis
-- This table stores the results of the data analysis.
CREATE TABLE stock_analysis (
    id SERIAL PRIMARY KEY,                                  -- Unique identifier for each analysis record
    ticker VARCHAR(10) NOT NULL,                            -- Stock ticker symbol
    analysis_date DATE NOT NULL,                            -- Date when the analysis was performed
    analysis_type VARCHAR(50) NOT NULL,                     -- Type of analysis performed
    result JSONB NOT NULL                                   -- Result of the analysis stored in JSON format
);

-- Table: analysis_types
-- This table defines the different types of analyses that can be performed.
CREATE TABLE analysis_types (
    id SERIAL PRIMARY KEY,                           -- Unique identifier for each analysis type
    type_name VARCHAR(50) UNIQUE NOT NULL,           -- Name of the analysis type
    description TEXT                                 -- Description of the analysis type
);

-- Table: api_keys
-- This table stores API keys for accessing the RESTful API.
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,                           -- Unique identifier for each API key
    user_id INTEGER NOT NULL,                        -- User ID to whom the API key belongs
    api_key VARCHAR(255) UNIQUE NOT NULL,            -- API key
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Creation timestamp
    last_used TIMESTAMP,                             -- Last used timestamp
    is_active BOOLEAN DEFAULT TRUE                   -- Status of the API key
);

-- Table: users
-- This table stores user information for those accessing the system.
CREATE TABLE users (
    id SERIAL PRIMARY KEY,                           -- Unique identifier for each user
    username VARCHAR(50) UNIQUE NOT NULL,            -- Username
    password_hash VARCHAR(255) NOT NULL,             -- Hashed password
    email VARCHAR(100) UNIQUE NOT NULL,              -- Email address
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Creation timestamp
    last_login TIMESTAMP                             -- Last login timestamp
);

-- Table: logs
-- This table stores logs for data processing and analysis activities.
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,                           -- Unique identifier for each log entry
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- Log date and time
    level VARCHAR(10) NOT NULL,                      -- Log level (e.g., INFO, ERROR)
    message TEXT NOT NULL,                           -- Log message
    details JSONB                                    -- Additional details stored in JSON format
);
