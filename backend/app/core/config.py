from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # OpenRouter AI
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_DEFAULT_MODEL: str
    
    # Redis
    REDIS_URL: str
    
    # Java gRPC
    JAVA_GRPC_HOST: str
    JAVA_GRPC_PORT: int
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # CORS
    ALLOWED_ORIGINS: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


