-- Alterix: Fix Database Permissions
-- Since the backend uses a single Supabase key (often anon), we need to ensure it has full access.

-- Grant full access to anon and authenticated roles
GRANT ALL ON SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Disable Row Level Security (RLS) on all tables so the backend can freely insert/update
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE skills DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_offered_skills DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_requested_skills DISABLE ROW LEVEL SECURITY;
ALTER TABLE exchanges DISABLE ROW LEVEL SECURITY;
ALTER TABLE exchange_participants DISABLE ROW LEVEL SECURITY;
ALTER TABLE exchange_offerings DISABLE ROW LEVEL SECURITY;
ALTER TABLE messages DISABLE ROW LEVEL SECURITY;
ALTER TABLE ratings DISABLE ROW LEVEL SECURITY;
ALTER TABLE notifications DISABLE ROW LEVEL SECURITY;
ALTER TABLE agent_traces DISABLE ROW LEVEL SECURITY;

-- Reload postgrest cache
NOTIFY pgrst, 'reload schema';
