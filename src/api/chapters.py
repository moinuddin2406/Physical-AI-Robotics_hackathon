from fastapi import APIRouter, HTTPException, Body
from typing import List
import json
from pathlib import Path

from models.chapter import Chapter, Exercise

router = APIRouter()

# Base path for chapter content
DOCS_PATH = Path("docs")


def load_chapter_metadata(chapter_id: str) -> dict:
    """Load chapter metadata from the docs directory"""
    metadata_path = DOCS_PATH / chapter_id / "metadata.json"

    if not metadata_path.exists():
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_id} not found")

    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_chapter_content(chapter_id: str) -> str:
    """Load chapter content from the docs directory"""
    content_path = DOCS_PATH / chapter_id / "README.md"

    if not content_path.exists():
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_id} content not found")

    with open(content_path, 'r', encoding='utf-8') as f:
        return f.read()


@router.get("/chapters", response_model=dict)
async def list_chapters():
    """Get a list of all available textbook chapters."""
    chapters = []

    for chapter_dir in DOCS_PATH.iterdir():
        if chapter_dir.is_dir():
            metadata_path = chapter_dir / "metadata.json"

            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                # Create a simplified chapter representation for the list
                chapter_summary = {
                    "id": metadata["id"],
                    "title": metadata["title"],
                    "description": metadata.get("key_concepts", ["No description available"])[0]
                                if metadata.get("key_concepts")
                                else "No description available",
                    "word_count": metadata["word_count"],
                    "position": metadata["position"]
                }
                chapters.append(chapter_summary)

    # Sort chapters by position
    chapters.sort(key=lambda x: x["position"])

    return {"chapters": chapters}


@router.get("/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter_details(chapter_id: str):
    """Get detailed information about a specific chapter."""
    # Load chapter metadata
    metadata = load_chapter_metadata(chapter_id)

    # Load chapter content
    content = load_chapter_content(chapter_id)

    # Create chapter object
    # Note: In a real implementation, exercises would be stored separately
    chapter = Chapter(
        id=metadata["id"],
        title=metadata["title"],
        slug=metadata["slug"],
        content=content,
        word_count=metadata["word_count"],
        learning_objectives=metadata.get("learning_objectives", []),
        key_concepts=metadata.get("key_concepts", []),
        prerequisites=metadata.get("prerequisites", []),
        related_chapters=metadata.get("related_chapters", []),
        exercises=[],  # Exercises would be loaded separately in a real implementation
        metadata=metadata
    )

    return chapter


@router.get("/chapters/{chapter_id}/exercises", response_model=dict)
async def get_chapter_exercises(chapter_id: str):
    """Get exercises for a specific chapter."""
    # Verify chapter exists
    metadata = load_chapter_metadata(chapter_id)

    # In this implementation, exercises are not stored separately
    # In a real implementation, they would be stored in a separate file or database
    # For now, we'll return an empty list
    return {
        "chapter_id": chapter_id,
        "exercises": []  # Would be populated from exercise files in a real implementation
    }


@router.post("/exercises/{exercise_id}/submit", response_model=dict)
async def submit_exercise_answer(exercise_id: str, request: dict = Body(...)):
    """Submit an answer to an exercise and get feedback."""
    answer = request.get("answer", "")
    user_id = request.get("user_id")

    # In a real implementation, this would:
    # 1. Look up the exercise by ID
    # 2. Validate the submitted answer
    # 3. Provide feedback

    # For this demonstration, we'll return a mock response
    return {
        "exercise_id": exercise_id,
        "is_correct": False,  # Would be determined by actual validation
        "feedback": "Exercise submission received. In a complete implementation, your answer would be validated.",
        "explanation": "This is a mock response. In a complete implementation, your answer would be compared to the correct answer and appropriate feedback would be provided."
    }