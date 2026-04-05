from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.agents.mediator import AgentMediator
from app.api.v1 import matches, exchanges, auth, skills, users, messages, ratings, notifications, traces
from app.core.config import settings
from app.core.database import get_supabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global mediator instance
mediator = None


async def seed_skills_on_startup(supabase):
    """Seed skills catalog if empty"""
    try:
        existing = supabase.table('skills').select('id').limit(1).execute()
        if not existing.data:
            from app.api.v1.skills import SEED_SKILLS
            import uuid
            skills_to_insert = []
            for skill in SEED_SKILLS:
                skills_to_insert.append({
                    'id': str(uuid.uuid4()),
                    **skill,
                    'valuation_score': 0.0
                })
            
            batch_size = 10
            for i in range(0, len(skills_to_insert), batch_size):
                batch = skills_to_insert[i:i + batch_size]
                supabase.table('skills').insert(batch).execute()
            
            logger.info(f"✅ Seeded {len(skills_to_insert)} skills into catalog")
        else:
            logger.info("✅ Skills catalog already populated")
    except Exception as e:
        logger.warning(f"⚠️  Failed to seed skills: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global mediator
    logger.info("Starting Alterix AI Engine...")
    
    # Test Supabase connection
    supabase = get_supabase()
    if supabase:
        logger.info("✅ Supabase connected successfully")
        # Auto-seed skills on startup
        await seed_skills_on_startup(supabase)
    else:
        logger.warning("⚠️  Supabase not configured — database features disabled")
    
    # Initialize AI agents
    mediator = AgentMediator()
    
    # Set mediator in route modules
    matches.set_mediator(mediator)
    exchanges.set_mediator(mediator)
    ratings.set_mediator(mediator)
    
    logger.info("✅ Alterix AI Engine started successfully")
    
    yield
    
    logger.info("Shutting down Alterix AI Engine...")


app = FastAPI(
    title="Alterix AI Engine",
    description="AI-powered skill exchange platform backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
allowed_origins = settings.ALLOWED_ORIGINS.split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📥 {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"📤 {request.method} {request.url.path} — {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"❌ {request.method} {request.url.path} — Error: {e}")
        raise


# Register all routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(skills.router, prefix="/api/v1", tags=["skills"])
app.include_router(matches.router, prefix="/api/v1", tags=["matches"])
app.include_router(exchanges.router, prefix="/api/v1", tags=["exchanges"])
app.include_router(messages.router, prefix="/api/v1", tags=["messages"])
app.include_router(ratings.router, prefix="/api/v1", tags=["ratings"])
app.include_router(notifications.router, prefix="/api/v1", tags=["notifications"])
app.include_router(traces.router, prefix="/api/v1", tags=["traces"])

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error caught: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "SYSTEM_ERROR",
            "message": "An unexpected error occurred in the Agent System.",
            "details": str(exc)
        }
    )


@app.get("/")
async def root():
    return {
        "service": "Alterix AI Engine",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "skills": "/api/v1/skills",
            "matches": "/api/v1/matches",
            "exchanges": "/api/v1/exchanges",
            "messages": "/api/v1/messages",
            "ratings": "/api/v1/ratings",
            "notifications": "/api/v1/notifications",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    supabase = get_supabase()
    db_status = "connected" if supabase else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "agents": mediator.get_agent_stats() if mediator else {}
    }


@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    """WebSocket endpoint for real-time notifications"""
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({
                "type": "notification",
                "message": f"Received: {data}"
            })
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
