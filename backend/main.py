from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import chapters, rag
from .config.settings import settings

# Initialize the RAG service
from .services.rag_service import RAGService
rag_service = RAGService()

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="API for the Physical AI & Humanoid Robotics textbook project, including RAG functionality",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chapters.router, prefix="/api", tags=["chapters"])
app.include_router(rag.router, prefix="/api", tags=["rag"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-12-13T10:00:00Z"}

# Make the RAG service available to other modules
app.state.rag_service = rag_service