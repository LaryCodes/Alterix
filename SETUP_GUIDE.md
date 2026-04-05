# Alterix - Complete Setup Guide

This guide will help team members set up the Alterix project from scratch.

## Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Node.js**: 18.x or higher
- **npm**: 9.x or higher (comes with Node.js)
- **PostgreSQL**: 14.x or higher (via Supabase)
- **Git**: Latest version

### Optional
- **Docker**: For containerized deployment
- **Redis**: For caching (optional)

## Project Structure

```
alterix/
├── backend/          # FastAPI Python backend
├── frontend/         # Next.js React frontend
├── core-engine/      # Java core engine 
├── database/         # SQL schemas
└── docs/            # Documentation
```

---

## Backend Setup (Python/FastAPI)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# OpenRouter AI Configuration
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_DEFAULT_MODEL=anthropic/claude-3.5-sonnet

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379

# Java gRPC Configuration (Optional)
JAVA_GRPC_HOST=localhost
JAVA_GRPC_PORT=50051

# Security
SECRET_KEY=your-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 5. Database Setup

#### Option A: Using Supabase (Recommended)

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Copy your project URL and anon key to `.env`
4. Run the SQL schema:
   ```bash
   # Copy contents of database/schema.sql
   # Paste into Supabase SQL Editor
   # Execute
   ```

#### Option B: Local PostgreSQL

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE alterix;
   ```
3. Run schema:
   ```bash
   psql -U postgres -d alterix -f ../database/schema.sql
   ```

### 6. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.10+

# Check installed packages
pip list

# Verify all dependencies
pip check
```

### 7. Run Backend Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Backend will be available at: http://localhost:8000

API Documentation: http://localhost:8000/docs

---

## Frontend Setup (Next.js/React)

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

If you encounter issues, try:
```bash
npm install --legacy-peer-deps
```

### 3. Environment Configuration

Create a `.env.local` file in the `frontend/` directory:

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 4. Verify Installation

```bash
# Check Node.js version
node --version  # Should be 18+

# Check npm version
npm --version

# List installed packages
npm list --depth=0
```

### 5. Run Frontend Development Server

```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

### 6. Build for Production

```bash
npm run build
npm start
```

---

## Complete Dependency List

### Backend (Python)

All dependencies are in `backend/requirements.txt`:

```txt
# Web Framework
fastapi==0.115.0
uvicorn[standard]==0.32.0

# Data Validation
pydantic==2.12.5
pydantic-settings==2.5.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
argon2-cffi==25.1.0

# File Upload
python-multipart==0.0.12

# WebSocket
websockets==13.1

# gRPC (Optional)
grpcio==1.68.0
grpcio-tools==1.68.0

# AI/ML
openai==1.54.0
numpy==2.1.3
scikit-learn==1.5.2

# Database
supabase==2.28.3
sqlalchemy==2.0.36
asyncpg==0.30.0

# Caching (Optional)
redis==5.2.0

# Utilities
python-dotenv==1.0.1
httpx==0.27.2
email-validator==2.3.0
```

### Frontend (Node.js)

All dependencies are in `frontend/package.json`:

```json
{
  "dependencies": {
    "@react-three/drei": "^9.92.0",
    "@react-three/fiber": "^8.15.11",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "axios": "^1.6.2",
    "clsx": "^2.0.0",
    "framer-motion": "^10.16.5",
    "lucide-react": "^0.294.0",
    "next": "14.0.3",
    "postcss": "^8",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hot-toast": "^2.4.1",
    "sonner": "^2.0.7",
    "tailwind-merge": "^2.1.0",
    "tailwindcss": "^3.3.0",
    "three": "^0.159.0",
    "typescript": "^5",
    "zustand": "^4.4.7"
  }
}
```

---

## Common Issues & Solutions

### Backend Issues

#### Issue: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: `Database connection failed`
```bash
# Solution: Check .env file
# Verify SUPABASE_URL and SUPABASE_KEY are correct
# Test connection at https://supabase.com
```

#### Issue: `Port 8000 already in use`
```bash
# Solution: Use different port
uvicorn app.main:app --reload --port 8001

# Or kill existing process
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

### Frontend Issues

#### Issue: `Module not found`
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Issue: `Port 3000 already in use`
```bash
# Solution: Use different port
PORT=3001 npm run dev

# Or kill existing process
# Windows: netstat -ano | findstr :3000
# Linux/Mac: lsof -ti:3000 | xargs kill
```

#### Issue: `Build fails with TypeScript errors`
```bash
# Solution: Check TypeScript version
npm install typescript@latest

# Or skip type checking (not recommended)
npm run build -- --no-lint
```

---

## Development Workflow

### 1. Start Backend
```bash
cd backend
source .venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload
```

### 2. Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

### 3. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## Docker Setup (Optional)

### Build and Run with Docker Compose
```bash
# From project root
docker-compose up --build

# Run in background
docker-compose up -d

# Stop containers
docker-compose down
```

---

## Production Deployment

### Backend Deployment

1. **Set environment variables** on your hosting platform
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run with Gunicorn**:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend Deployment

1. **Build application**: `npm run build`
2. **Deploy to Vercel/Netlify** or
3. **Run with PM2**:
   ```bash
   npm install -g pm2
   pm2 start npm --name "alterix-frontend" -- start
   ```

---

## Environment Variables Reference

### Backend Required Variables
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon key
- `OPENROUTER_API_KEY` - OpenRouter API key for AI
- `SECRET_KEY` - JWT secret (min 32 characters)
- `ALLOWED_ORIGINS` - CORS allowed origins

### Backend Optional Variables
- `REDIS_URL` - Redis connection string
- `JAVA_GRPC_HOST` - Java gRPC host
- `JAVA_GRPC_PORT` - Java gRPC port

### Frontend Required Variables
- `NEXT_PUBLIC_API_URL` - Backend API URL

---

## Getting API Keys

### Supabase
1. Go to https://supabase.com
2. Create account and new project
3. Copy URL and anon key from Settings > API

### OpenRouter
1. Go to https://openrouter.ai
2. Create account
3. Generate API key from dashboard

---

## Support & Resources

- **Documentation**: See `/docs` folder
- **API Reference**: http://localhost:8000/docs
- **Design System**: `frontend/DESIGN_SYSTEM.md`
- **Consistency Guide**: `frontend/CONSISTENCY_GUIDE.md`

---

## Quick Start Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Backend `.env` configured
- [ ] Supabase project created
- [ ] Database schema executed
- [ ] Frontend dependencies installed
- [ ] Frontend `.env.local` configured
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Can access http://localhost:3000
- [ ] Can register/login successfully

---

## Next Steps

1. Review the architecture documentation
2. Explore the API at http://localhost:8000/docs
3. Check the design system in `frontend/DESIGN_SYSTEM.md`
4. Start building features!

Happy coding! 🚀
