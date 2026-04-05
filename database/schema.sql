-- Alterix Database Schema for Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    trust_score DECIMAL(5,2) DEFAULT 50.0,
    total_exchanges INTEGER DEFAULT 0,
    successful_exchanges INTEGER DEFAULT 0,
    average_rating DECIMAL(3,2) DEFAULT 0.0,
    report_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Skills table
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    level VARCHAR(50) NOT NULL CHECK (level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT')),
    description TEXT,
    estimated_hours INTEGER DEFAULT 1,
    valuation_score DECIMAL(10,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User skills (offered)
CREATE TABLE user_offered_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(50) NOT NULL,
    years_experience INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

-- User skills (requested)
CREATE TABLE user_requested_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    desired_level VARCHAR(50) NOT NULL,
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, skill_id)
);

-- Exchanges table
CREATE TABLE exchanges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type VARCHAR(50) NOT NULL CHECK (type IN ('DIRECT_SWAP', 'PAID_LEARNING', 'MULTI_PARTY_CHAIN')),
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'NEGOTIATING', 'SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    fairness_score DECIMAL(5,2) DEFAULT 0.0,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exchange participants
CREATE TABLE exchange_participants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exchange_id UUID REFERENCES exchanges(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(exchange_id, user_id)
);

-- Exchange offerings
CREATE TABLE exchange_offerings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exchange_id UUID REFERENCES exchanges(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    hours_committed INTEGER DEFAULT 0,
    payment_amount DECIMAL(10,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sessions table
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exchange_id UUID REFERENCES exchanges(id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    status VARCHAR(50) NOT NULL DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    meeting_link TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ratings table
CREATE TABLE ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exchange_id UUID REFERENCES exchanges(id) ON DELETE CASCADE,
    rater_id UUID REFERENCES users(id) ON DELETE CASCADE,
    rated_id UUID REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(exchange_id, rater_id, rated_id)
);

-- Messages table (for chat)
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    exchange_id UUID REFERENCES exchanges(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trust connections (for trust graph)
CREATE TABLE trust_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    to_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    weight DECIMAL(5,2) DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(from_user_id, to_user_id)
);

-- Notifications table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT false,
    related_exchange_id UUID REFERENCES exchanges(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_trust_score ON users(trust_score);
CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_skills_name ON skills(name);
CREATE INDEX idx_exchanges_status ON exchanges(status);
CREATE INDEX idx_exchanges_type ON exchanges(type);
CREATE INDEX idx_messages_exchange ON messages(exchange_id);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_ratings_exchange ON ratings(exchange_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_exchanges_updated_at BEFORE UPDATE ON exchanges
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_trust_connections_updated_at BEFORE UPDATE ON trust_connections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_offered_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_requested_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE exchanges ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Users can read their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own data
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Users can view their own skills
CREATE POLICY "Users can view own offered skills" ON user_offered_skills
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own requested skills" ON user_requested_skills
    FOR SELECT USING (auth.uid() = user_id);

-- Users can view exchanges they're part of
CREATE POLICY "Users can view own exchanges" ON exchanges
    FOR SELECT USING (
        id IN (
            SELECT exchange_id FROM exchange_participants
            WHERE user_id = auth.uid()
        )
    );

-- Users can view messages in their exchanges
CREATE POLICY "Users can view exchange messages" ON messages
    FOR SELECT USING (
        exchange_id IN (
            SELECT exchange_id FROM exchange_participants
            WHERE user_id = auth.uid()
        )
    );

-- Users can view their own notifications
CREATE POLICY "Users can view own notifications" ON notifications
    FOR SELECT USING (auth.uid() = user_id);
