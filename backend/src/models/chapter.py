from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ExerciseType(str, Enum):
    multiple_choice = "multiple_choice"
    short_answer = "short_answer"
    practical = "practical"


class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Exercise(BaseModel):
    id: str
    type: ExerciseType
    question: str
    options: Optional[List[str]] = None  # For multiple choice questions
    answer: str
    explanation: Optional[str] = None
    difficulty: DifficultyLevel


class Chapter(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    word_count: int
    learning_objectives: List[str]
    key_concepts: List[str]
    prerequisites: List[str]
    related_chapters: List[str]
    exercises: List[Exercise]
    metadata: Dict[str, Any]


class DocumentChunk(BaseModel):
    id: str
    chapter_id: str
    content: str
    chunk_index: int
    embedding: Optional[List[float]] = None  # Vector representation of the content
    metadata: Dict[str, Any]


class QueryRequest(BaseModel):
    query: str
    options: Optional[Dict[str, Any]] = {
        "response_complexity": "intermediate",
        "language": "en",
        "use_personalization": False,
        "max_chunks": 3
    }


class QueryResult(BaseModel):
    chunk_id: str
    chapter_id: str
    content: str
    similarity_score: float
    metadata: Dict[str, Any]


class QueryResponse(BaseModel):
    response: str
    source_chapters: List[str]
    confidence: float
    chunks_used: int
    query_id: str


class UserPreferences(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    response_complexity: str = "intermediate"
    language_preference: str = "en"
    personalization_enabled: bool = False