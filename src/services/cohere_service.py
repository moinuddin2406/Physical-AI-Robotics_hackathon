"""
Cohere service for embeddings and text generation
"""
from typing import List, Optional
import cohere
import numpy as np
from config.settings import settings


class CohereService:
    """
    Service for handling Cohere API calls for embeddings and text generation
    """

    def __init__(self):
        # Initialize the Cohere API with the API key
        if not settings.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(settings.COHERE_API_KEY)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        # Cohere's embed endpoint has a limit on the number of texts per request
        # So we need to batch them
        batch_size = 96  # Conservative batch size to stay under limits
        embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            # Filter out empty texts
            filtered_batch = [text for text in batch if text.strip()]
            
            if not filtered_batch:
                # Add zero embeddings for empty texts
                for text in batch:
                    if not text.strip():
                        embeddings.append([0.0] * settings.EMBEDDING_DIMENSIONS)
                continue

            # Generate embeddings for the batch
            response = self.client.embed(
                texts=filtered_batch,
                model=settings.COHERE_EMBEDDING_MODEL,
                input_type="search_document"
            )

            # Add embeddings to the result list
            batch_embeddings = response.embeddings
            batch_idx = 0
            
            for text in batch:
                if text.strip():  # Non-empty text
                    embeddings.append(batch_embeddings[batch_idx])
                    batch_idx += 1
                else:  # Empty text
                    embeddings.append([0.0] * settings.EMBEDDING_DIMENSIONS)

        return embeddings

    def get_query_embedding(self, query: str) -> List[float]:
        """
        Generate a single embedding for a query using Cohere
        """
        if not query.strip():
            return [0.0] * settings.EMBEDDING_DIMENSIONS

        response = self.client.embed(
            texts=[query],
            model=settings.COHERE_EMBEDDING_MODEL,
            input_type="search_query"
        )

        return response.embeddings[0]

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response using Cohere's generate endpoint
        Note: For production use, you might want to use a different LLM for generation
        since Cohere's generation capabilities might differ from Gemini
        """
        try:
            response = self.client.generate(
                model='command-r-plus',  # Using Cohere's command-r-plus model for generation
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            return response.generations[0].text
        except Exception as e:
            # Fallback response in case of error
            return f"Error generating response: {str(e)}"