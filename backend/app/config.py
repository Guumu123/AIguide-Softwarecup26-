from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AI 景区向导 APP")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/scenic_guide")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-super-secret-key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # AI Services
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY", "")
    FUNASR_URL: str = os.getenv("FUNASR_URL", "http://localhost:10010")
    TTS_URL: str = os.getenv("TTS_URL", "http://localhost:10020")

settings = Settings()
