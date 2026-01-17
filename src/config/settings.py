try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/textbook"

    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    # Google Gemini settings (for LLM responses)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_LLM_MODEL: str = "gemini-1.5-flash"

    # Cohere settings (for embeddings)
    COHERE_API_KEY: Optional[str] = None
    COHERE_EMBEDDING_MODEL: str = "embed-multilingual-v3.0"
    EMBEDDING_DIMENSIONS: int = 1024  # for Cohere embed-multilingual-v3.0

    # API settings
    ALLOWED_ORIGINS: List[str] = ["*"]  # In production, specify actual origins

    # RAG settings
    MAX_RETRIEVAL_CHUNKS: int = 5
    MIN_CONFIDENCE_SCORE: float = 0.5

    # Content processing settings
    CHUNK_SIZE: int = 512  # tokens
    OVERLAP_SIZE: int = 64  # tokens

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()