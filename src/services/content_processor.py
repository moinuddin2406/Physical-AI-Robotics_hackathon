"""
Content processing service for the Physical AI & Humanoid Robotics textbook
Handles chunking of textbook content and preparation for RAG system
"""
import os
import json
import re
from typing import List, Dict, Any
from pathlib import Path

from models.chapter import Chapter, DocumentChunk
from config.settings import settings


class ContentProcessor:
    """
    Service for processing textbook content for the RAG system
    """
    
    def __init__(self):
        self.docs_path = Path("docs")
        self.chunk_size = settings.CHUNK_SIZE
        self.overlap_size = settings.OVERLAP_SIZE
    
    def load_chapters(self) -> List[Dict[str, Any]]:
        """
        Load all chapters from the docs/ directory
        """
        chapters = []
        
        for chapter_dir in self.docs_path.iterdir():
            if chapter_dir.is_dir():
                readme_path = chapter_dir / "README.md"
                metadata_path = chapter_dir / "metadata.json"
                
                if readme_path.exists() and metadata_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    chapter_data = {
                        "id": metadata["id"],
                        "title": metadata["title"],
                        "slug": metadata["slug"],
                        "content": content,
                        "metadata": metadata
                    }
                    
                    chapters.append(chapter_data)
        
        # Sort chapters by position
        chapters.sort(key=lambda x: x["metadata"]["position"])
        return chapters
    
    def chunk_content(self, content: str, chapter_id: str) -> List[DocumentChunk]:
        """
        Split content into chunks for RAG system
        """
        # Split content into sentences or paragraphs
        # This is a simplified approach - in practice, you might want more sophisticated chunking
        paragraphs = re.split(r'\n\s*\n', content)
        
        chunks = []
        chunk_id = 0
        
        for para in paragraphs:
            if len(para.strip()) == 0:
                continue
                
            # If paragraph is too large, split into smaller parts
            if len(para) > self.chunk_size:
                sentences = re.split(r'(?<=[.!?]) +', para)
                current_chunk = ""
                
                for sentence in sentences:
                    if len(current_chunk + " " + sentence) <= self.chunk_size:
                        current_chunk += " " + sentence
                    else:
                        if current_chunk:
                            chunks.append(
                                DocumentChunk(
                                    id=f"{chapter_id}_chunk_{chunk_id}",
                                    chapter_id=chapter_id,
                                    content=current_chunk.strip(),
                                    chunk_index=chunk_id,
                                    metadata={"source": chapter_id}
                                )
                            )
                            chunk_id += 1
                        current_chunk = sentence
                
                if current_chunk:
                    chunks.append(
                        DocumentChunk(
                            id=f"{chapter_id}_chunk_{chunk_id}",
                            chapter_id=chapter_id,
                            content=current_chunk.strip(),
                            chunk_index=chunk_id,
                            metadata={"source": chapter_id}
                        )
                    )
                    chunk_id += 1
            else:
                chunks.append(
                    DocumentChunk(
                        id=f"{chapter_id}_chunk_{chunk_id}",
                        chapter_id=chapter_id,
                        content=para.strip(),
                        chunk_index=chunk_id,
                        metadata={"source": chapter_id}
                    )
                )
                chunk_id += 1
        
        return chunks
    
    def process_all_content(self) -> List[DocumentChunk]:
        """
        Process all textbook content and return chunks for RAG system
        """
        all_chunks = []
        
        chapters = self.load_chapters()
        
        for chapter in chapters:
            chunks = self.chunk_content(chapter["content"], chapter["id"])
            all_chunks.extend(chunks)
        
        return all_chunks


# Example usage
if __name__ == "__main__":
    processor = ContentProcessor()
    chunks = processor.process_all_content()
    
    print(f"Processed {len(chunks)} content chunks from textbook")
    
    # Print first few chunks as example
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1} (Chapter: {chunk.chapter_id}):")
        print(f"Content preview: {chunk.content[:100]}...")