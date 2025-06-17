-- ===========================================
-- SQL Script to Create statistics_results Table
-- ===========================================
-- This script creates the statistics_results table for storing computed statistical values
-- from the statistics_service application.
--
-- Table Purpose:
-- - Store computed statistical results (z-score, correlation, cointegration)
-- - Track which symbol and timeframe each statistic was computed for
-- - Record when each statistic was calculated
-- - Allow for efficient querying and historical analysis

CREATE TABLE IF NOT EXISTS statistics_results (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timeframe VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    value DECIMAL(15,8) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_statistics_results_symbol ON statistics_results(symbol);
CREATE INDEX IF NOT EXISTS idx_statistics_results_timeframe ON statistics_results(timeframe);
CREATE INDEX IF NOT EXISTS idx_statistics_results_name ON statistics_results(name);
CREATE INDEX IF NOT EXISTS idx_statistics_results_timestamp ON statistics_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_statistics_results_symbol_timeframe_name ON statistics_results(symbol, timeframe, name);

-- Add comments for documentation
COMMENT ON TABLE statistics_results IS 'Stores computed statistical results from the statistics service';
COMMENT ON COLUMN statistics_results.id IS 'Primary key auto-increment identifier';
COMMENT ON COLUMN statistics_results.symbol IS 'Stock symbol (e.g., SPY, AAPL)';
COMMENT ON COLUMN statistics_results.timeframe IS 'Bar size timeframe (e.g., 5 mins, 1 hour)';
COMMENT ON COLUMN statistics_results.name IS 'Type of statistic (zscore, correlation, cointegration)';
COMMENT ON COLUMN statistics_results.value IS 'Computed statistical value with high precision';
COMMENT ON COLUMN statistics_results.timestamp IS 'When the statistic was calculated';
COMMENT ON COLUMN statistics_results.created_at IS 'When the record was inserted into the database';
COMMENT ON COLUMN statistics_results.updated_at IS 'When the record was last updated';