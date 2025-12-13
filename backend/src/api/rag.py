from fastapi import APIRouter, Request
from ..models.chapter import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def rag_query(query_request: QueryRequest, request: Request):
    """Submit a query to the RAG system and receive a response based on textbook content."""
    # Get the RAG service from app state
    rag_service = request.app.state.rag_service

    # Process the query using the RAG service
    response = rag_service.query(query_request)

    return response