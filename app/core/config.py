from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    # OpenRouter AI
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_DEFAULT_MODEL: str = "anthropic/claude-3.5-sonnet"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Java gRPC
    JAVA_GRPC_HOST: str = "localhost"
    JAVA_GRPC_PORT: int = 50051
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

