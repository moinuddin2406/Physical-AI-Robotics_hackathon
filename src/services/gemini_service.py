"""
Google Gemini service for embeddings and text generation
"""
from typing import List, Optional
import google.generativeai as genai
import numpy as np
from config.settings import settings


class GeminiService:
    """
    Service for handling Google Gemini API calls for embeddings and text generation
    """

    def __init__(self):
        # Initialize the Gemini API with the API key
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Initialize the LLM model
        self.llm_model = genai.GenerativeModel(settings.GEMINI_LLM_MODEL)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Google Gemini
        """
        embeddings = []
        
        for text in texts:
            # Skip empty texts
            if not text.strip():
                embeddings.append([0.0] * settings.EMBEDDING_DIMENSIONS)
                continue
            
            # Generate embedding for the text
            response = genai.embed_content(
                model=settings.GEMINI_EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            
            embedding = response['embedding']
            embeddings.append(embedding)
        
        return embeddings

    def get_query_embedding(self, query: str) -> List[float]:
        """
        Generate a single embedding for a query using Google Gemini
        """
        if not query.strip():
            return [0.0] * settings.EMBEDDING_DIMENSIONS
        
        response = genai.embed_content(
            model=settings.GEMINI_EMBEDDING_MODEL,
            content=query,
            task_type="retrieval_query"
        )
        
        return response['embedding']

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using Google Gemini LLM
        """
        try:
            response = self.llm_model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback response in case of error
            return f"Error generating response: {str(e)}"