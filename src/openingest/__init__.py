"""
OpenIngest - Open-source document ingestion library
Simple, self-hosted alternative to LlamaParse powered by IBM Docling
"""

from .ingestor import OpenIngestor
from .models import IngestedDocument, IngestConfig, OutputFormat

__version__ = "0.1.0"
__all__ = ["OpenIngestor", "IngestedDocument", "IngestConfig", "OutputFormat"]