"""
OpenIngestor - Main ingestion class powered by Docling
Simple, self-hosted document ingestion like LlamaParse
"""

import time
from pathlib import Path
from typing import Union, Optional

from docling.document_converter import DocumentConverter

from .models import IngestedDocument, IngestConfig, OutputFormat


class OpenIngestor:
    """
    Open-source document ingestor powered by IBM Docling
    
    Usage:
        ingestor = OpenIngestor()
        result = ingestor.ingest("document.pdf")
        print(result.content)
    """
    
    def __init__(self, config: Optional[IngestConfig] = None):
        """Initialize the ingestor with optional configuration"""
        self.config = config or IngestConfig()
        self.converter = DocumentConverter()
        
    def ingest(self, document_path: Union[str, Path]) -> IngestedDocument:
        """
        Ingest a document using Docling
        
        Args:
            document_path: Path to the document file
            
        Returns:
            IngestedDocument: Ingested result with content and metadata
        """
        document_path = Path(document_path)
        
        if not document_path.exists():
            raise FileNotFoundError(f"Document not found: {document_path}")
            
        # Check if format is supported
        if not self._is_supported(document_path):
            raise ValueError(f"Unsupported format: {document_path.suffix}")
        
        # Ingest with timing
        start_time = time.time()
        result = self.converter.convert(str(document_path))
        processing_time = time.time() - start_time
        
        # Extract content based on format
        content = self._extract_content(result, self.config.output_format)
        
        return IngestedDocument(
            content=content,
            filename=document_path.name,
            page_count=len(result.document.pages),
            processing_time=processing_time,
            format=self.config.output_format,
            file_size=document_path.stat().st_size
        )
    
    def ingest_from_bytes(self, file_bytes: bytes, filename: str) -> IngestedDocument:
        """
        Ingest document from bytes
        
        Args:
            file_bytes: Document content as bytes
            filename: Original filename for format detection
            
        Returns:
            IngestedDocument: Ingested result
        """
        # Create temporary file
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            result = self.ingest(tmp_file_path)
            result.filename = filename  # Use original filename
            result.file_size = len(file_bytes)
            return result
        finally:
            os.unlink(tmp_file_path)
    
    def ingest_directory(self, directory_path: Union[str, Path], pattern: str = "*") -> list[IngestedDocument]:
        """
        Ingest all supported documents in a directory
        
        Args:
            directory_path: Path to directory
            pattern: File pattern to match (default: all files)
            
        Returns:
            List of IngestedDocument results
        """
        directory_path = Path(directory_path)
        results = []
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and self._is_supported(file_path):
                try:
                    result = self.ingest(file_path)
                    results.append(result)
                except Exception as e:
                    print(f"⚠️  Failed to ingest {file_path.name}: {e}")
        
        return results
    
    def _extract_content(self, result, output_format: OutputFormat) -> str:
        """Extract content in the specified format"""
        if output_format == OutputFormat.MARKDOWN:
            return result.document.export_to_markdown()
        elif output_format == OutputFormat.HTML:
            return result.document.export_to_html()
        elif output_format == OutputFormat.JSON:
            return result.document.export_to_json()
        else:  # TEXT
            # Fallback to markdown if text export not available
            return result.document.export_to_text() if hasattr(result.document, 'export_to_text') else result.document.export_to_markdown()
    
    def _is_supported(self, path: Path) -> bool:
        """Check if file format is supported by Docling"""
        supported = {'.pdf', '.docx', '.pptx', '.xlsx', '.html', '.md', '.csv'}
        return path.suffix.lower() in supported
    
    @classmethod
    def quick_ingest(cls, document_path: Union[str, Path]) -> str:
        """
        Quick ingest - just return the content string
        
        Usage:
            content = OpenIngestor.quick_ingest("doc.pdf")
        """
        ingestor = cls()
        result = ingestor.ingest(document_path)
        return result.content