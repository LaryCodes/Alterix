-- Alterix Phase 2 Database Upgrade
-- Run this in your Supabase SQL Editor

-- 1. Create the agent_traces table for explainability
CREATE TABLE IF NOT EXISTS agent_traces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exchange_id UUID REFERENCES exchanges(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    input_data JSONB NOT NULL,
    output_data JSONB NOT NULL,
    metrics JSONB, -- stores skill_match, trust_score, final_score etc.
    decision_reasoning TEXT NOT NULL,
    execution_time_ms INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for fast lookup by exchange_id for the UI panel
CREATE INDEX IF NOT EXISTS idx_agent_traces_exchange ON agent_traces(exchange_id);

-- Optional: If you ever search by specific agent
CREATE INDEX IF NOT EXISTS idx_agent_traces_name ON agent_traces(agent_name);

-- Ensure postgrest cache is reloaded
NOTIFY pgrst, 'reload schema';
