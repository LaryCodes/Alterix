from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.agents.mediator import AgentMediator
from app.api.v1 import matches, exchanges
from app.core.config import settings
from app.core.database import get_supabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global mediator instance
mediator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global mediator
    logger.info("Starting Alterix AI Engine...")
    
    # Test Supabase connection
    supabase = get_supabase()
    if supabase:
        logger.info("✅ Supabase connected successfully")
    else:
        logger.warning("⚠️  Supabase not configured - using mock data")
    
    # Initialize AI agents
    mediator = AgentMediator()
    
    # Set mediator in route modules
    matches.set_mediator(mediator)
    exchanges.set_mediator(mediator)
    
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
    response = await call_next(request)
    logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code}")
    return response

# Include routers
app.include_router(matches.router, prefix="/api/v1", tags=["matches"])
app.include_router(exchanges.router, prefix="/api/v1", tags=["exchanges"])

# Import and include auth router
from app.api.v1 import auth, skills, users
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(skills.router, prefix="/api/v1", tags=["skills"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])


@app.get("/")
async def root():
    return {
        "service": "Alterix AI Engine",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
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
            # Echo for now - in production, handle real notifications
            await websocket.send_json({
                "type": "notification",
                "message": f"Received: {data}"
            })
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
