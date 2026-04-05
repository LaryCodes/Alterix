# Alterix - Quick Setup

## ✅ Your .env is configured correctly!

**Rule: NEVER use quotes in .env files**

```env
GOOD: SUPABASE_URL=https://example.supabase.co
BAD:  SUPABASE_URL="https://example.supabase.co"
```

## 🗄️ Create Database Tables

1. Go to your Supabase project: https://supabase.com/dashboard
2. Click **SQL Editor** in left sidebar
3. Click **New query**
4. Copy ALL content from `create_tables.sql`
5. Paste and click **Run** (or Ctrl+Enter)
6. Done! Tables created.

## 🔑 Add OpenRouter API Key

1. Get key from: https://openrouter.ai/keys
2. Copy the key (starts with `sk-or-v1-`)
3. In `backend/.env`, replace:
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   ```
   with your actual key (NO quotes)

## ✅ Verify Code Uses Environment Variables

All code properly uses `settings` from config:
- ✅ `app/core/config.py` - Reads from .env
- ✅ `app/core/database.py` - Uses `settings.SUPABASE_URL`
- ✅ `app/services/openrouter_service.py` - Uses `settings.OPENROUTER_API_KEY`
- ✅ `app/main.py` - Uses `settings.ALLOWED_ORIGINS`

NO hardcoded values anywhere!

## 🚀 Run

```bash
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

You should see:
```
INFO:app.core.database:Supabase client initialized successfully
INFO:app.main:✅ Alterix AI Engine started successfully
```

## 🧪 Test

```bash
curl http://localhost:8000/health
```

Done!
