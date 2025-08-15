# 🚀 OpenIngest

**Open-source document ingestion library** - Self-hosted alternative to LlamaParse

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/openingest/openingest)

---

## 🎯 Why OpenIngest?

**Same simplicity as LlamaParse, but self-hosted and private.**

```python
# LlamaParse (cloud, costs money, sends your data away)
from llama_parse import LlamaParse
parser = LlamaParse(api_key="llx-...")
docs = parser.load_data("document.pdf")

# OpenIngest (self-hosted, free, keeps your data)
from openingest import OpenIngestor  
ingestor = OpenIngestor()
result = ingestor.ingest("document.pdf")
```

## 📊 OpenIngest vs LlamaParse

| Feature | OpenIngest | LlamaParse |
|---------|------------|------------|
| **🏠 Hosting** | Self-hosted | Cloud only |
| **🔒 Privacy** | Your data stays local | Data sent to LlamaIndex |
| **💰 Cost** | Free (infrastructure only) | $0.003/page |
| **⚡ Speed** | Local processing | API calls |
| **🛠️ Customization** | Full control | Limited |
| **📱 Offline** | Works offline | Requires internet |
| **📄 Formats** | PDF, DOCX, PPTX, XLSX, HTML, MD | Primarily PDF |

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Pull and run
docker run -v $(pwd):/docs openingest/openingest python -c "
from openingest import OpenIngestor
result = OpenIngestor().ingest('/docs/your-document.pdf')
print(result.content)
"
```

### Option 2: Python Package

```bash
pip install openingest
```

```python
from openingest import OpenIngestor

# Simple usage
content = OpenIngestor.quick_ingest("document.pdf")
print(content)

# Full usage with metadata
ingestor = OpenIngestor()
result = ingestor.ingest("document.pdf")

print(f"📄 {result.filename}")
print(f"📊 {result.page_count} pages")
print(f"⏱️  {result.processing_time:.2f}s")
print(result.content)
```

## 💡 Usage Examples

### Basic Document Ingestion

```python
from openingest import OpenIngestor, IngestConfig, OutputFormat

# Quick one-liner
content = OpenIngestor.quick_ingest("research.pdf")

# With configuration
config = IngestConfig(
    output_format=OutputFormat.MARKDOWN,
    extract_tables=True,
    extract_images=False
)

ingestor = OpenIngestor(config)
result = ingestor.ingest("research.pdf")

# Save result
result.save("research.md")
```

### Batch Processing

```python
ingestor = OpenIngestor()

# Process all PDFs in a directory
results = ingestor.ingest_directory("documents/", "*.pdf")

for result in results:
    print(f"✅ {result.filename}: {result.page_count} pages")
    result.save(f"processed/{result.filename}.md")
```

### RAG Pipeline Integration

```python
from openingest import OpenIngestor

class MyRAGPipeline:
    def __init__(self):
        self.ingestor = OpenIngestor()
        self.vector_store = YourVectorStore()
    
    def add_document(self, doc_path):
        # Ingest document
        result = self.ingestor.ingest(doc_path)
        
        # Split into chunks
        chunks = result.get_chunks(chunk_size=1000, overlap=100)
        
        # Add to vector store
        for chunk in chunks:
            self.vector_store.add(
                text=chunk,
                metadata={
                    "source": result.filename,
                    "pages": result.page_count,
                    "processing_time": result.processing_time
                }
            )
```

### Ingest from Bytes

```python
# Useful for web uploads or API integrations
with open("document.pdf", "rb") as f:
    file_bytes = f.read()

result = ingestor.ingest_from_bytes(file_bytes, "document.pdf")
print(result.content)
```

## 🐳 Docker Usage

### As Base Image

```dockerfile
FROM openingest/openingest:latest

# Your application
COPY app.py /app/
WORKDIR /app

# Use OpenIngest in your app
CMD ["python", "app.py"]
```

### With Docker Compose

```yaml
version: '3.8'
services:
  document-processor:
    image: openingest/openingest:latest
    volumes:
      - ./documents:/app/documents:ro
      - ./processed:/app/processed
    command: python -c "
      from openingest import OpenIngestor
      import os
      ingestor = OpenIngestor()
      for f in os.listdir('/app/documents'):
        if f.endswith('.pdf'):
          result = ingestor.ingest(f'/app/documents/{f}')
          result.save(f'/app/processed/{f}.md')
    "
```

## 📦 Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Portable Document Format |
| Word | `.docx` | Microsoft Word documents |
| PowerPoint | `.pptx` | Microsoft PowerPoint |
| Excel | `.xlsx` | Microsoft Excel spreadsheets |
| HTML | `.html` | Web pages |
| Markdown | `.md` | Markdown files |
| CSV | `.csv` | Comma-separated values |

## 🔧 Configuration

```python
from openingest import IngestConfig, OutputFormat

config = IngestConfig(
    output_format=OutputFormat.MARKDOWN,  # MARKDOWN, HTML, JSON, TEXT
    chunk_size=1000,                      # For auto-chunking
    extract_images=False,                 # Extract images
    extract_tables=True,                  # Extract tables
)

ingestor = OpenIngestor(config)
```

## 🚀 Deployment

### Production Docker Setup

```bash
# Build production image
docker build -t my-openingest .

# Run with resource limits
docker run -d \
  --name openingest \
  --memory=4g \
  --cpus=2 \
  -v /path/to/documents:/documents:ro \
  -v /path/to/output:/output \
  my-openingest
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openingest
spec:
  replicas: 3
  selector:
    matchLabels:
      app: openingest
  template:
    metadata:
      labels:
        app: openingest
    spec:
      containers:
      - name: openingest
        image: openingest/openingest:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

## 🔄 Migration from LlamaParse

**Before (LlamaParse):**
```python
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-your-key",
    result_type="markdown"
)

documents = parser.load_data("file.pdf")
content = documents[0].text
```

**After (OpenIngest):**
```python
from openingest import OpenIngestor, IngestConfig, OutputFormat

ingestor = OpenIngestor(IngestConfig(
    output_format=OutputFormat.MARKDOWN
))

result = ingestor.ingest("file.pdf")
content = result.content
```

**Migration benefits:**
- ✅ Remove API key dependency
- ✅ Eliminate per-page costs
- ✅ Keep data private and secure
- ✅ Work completely offline
- ✅ Same simple API!

## 📈 Performance

Typical processing times on standard hardware:

| Document Type | Pages | Time | Memory |
|---------------|-------|------|--------|
| PDF (text-heavy) | 10 | ~2s | ~500MB |
| PDF (image-heavy) | 10 | ~8s | ~1GB |
| DOCX | 20 | ~3s | ~400MB |
| PPTX | 15 slides | ~4s | ~600MB |

## 🤝 Contributing

We love contributions! OpenIngest is designed to be:

- **Simple**: Easy to use and understand
- **Fast**: Efficient processing
- **Reliable**: Robust error handling
- **Extensible**: Easy to add new features

```bash
# Development setup
git clone https://github.com/openingest/openingest
cd openingest
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/
```

## 📝 Roadmap

- [x] **Core ingestion** with Docling
- [x] **Multi-format support** (PDF, DOCX, PPTX, etc.)
- [x] **Docker containerization**
- [x] **Chunking for RAG**
- [ ] **Web UI** for document upload
- [ ] **REST API** service mode
- [ ] **OCR support** for scanned documents
- [ ] **Batch processing** improvements
- [ ] **Cloud storage** integrations (S3, GCS)

## 📄 License

MIT License - Use it however you want!

## 🌟 Star us on GitHub!

If OpenIngest saves you money and keeps your data private, please ⭐ star us on GitHub!

---

**OpenIngest** - Because your documents deserve privacy and you deserve to save money! 🚀