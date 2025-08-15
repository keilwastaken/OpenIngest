"""
Data models for OpenIngest
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class OutputFormat(Enum):
    MARKDOWN = "markdown"
    HTML = "html" 
    JSON = "json"
    TEXT = "text"


@dataclass
class IngestConfig:
    """Configuration for document ingestion"""
    output_format: OutputFormat = OutputFormat.MARKDOWN
    chunk_size: Optional[int] = None
    extract_images: bool = False
    extract_tables: bool = True
    

@dataclass
class IngestedDocument:
    """Result of document ingestion"""
    content: str
    filename: str
    page_count: int
    processing_time: float
    format: OutputFormat
    file_size: Optional[int] = None
    
    def save(self, filepath: str) -> None:
        """Save content to file"""
        Path(filepath).write_text(self.content, encoding='utf-8')
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "content": self.content,
            "filename": self.filename,
            "page_count": self.page_count,
            "processing_time": self.processing_time,
            "format": self.format.value,
            "file_size": self.file_size
        }
    
    def get_chunks(self, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
        """Split content into overlapping chunks for RAG"""
        if len(self.content) <= chunk_size:
            return [self.content]
        
        chunks = []
        start = 0
        
        while start < len(self.content):
            end = start + chunk_size
            chunk = self.content[start:end]
            
            # Try to break at word boundary
            if end < len(self.content):
                last_space = chunk.rfind(' ')
                if last_space > chunk_size * 0.8:  # If we find a space in the last 20%
                    chunk = chunk[:last_space]
                    end = start + last_space
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start >= len(self.content):
                break
                
        return [chunk for chunk in chunks if len(chunk.strip()) > 50]