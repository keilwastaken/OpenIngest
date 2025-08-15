"""
Basic usage examples for OpenIngest
Self-hosted document ingestion like LlamaParse
"""

from openingest import OpenIngestor, IngestConfig, OutputFormat

def main():
    """Basic usage examples"""
    
    # 1. Simplest usage - just get content
    print("🚀 Quick Ingest:")
    content = OpenIngestor.quick_ingest("documents/sample.md")
    print(f"Content preview: {content[:200]}...")
    
    print("\n" + "="*50)
    
    # 2. Full ingestion with metadata
    print("📄 Full Ingestion:")
    ingestor = OpenIngestor()
    result = ingestor.ingest("documents/sample.md")
    
    print(f"📄 File: {result.filename}")
    print(f"📊 Pages: {result.page_count}")
    print(f"⏱️  Time: {result.processing_time:.2f}s")
    print(f"📁 Size: {result.file_size} bytes")
    print(f"📝 Format: {result.format.value}")
    
    # Save result
    result.save("output.md")
    print("💾 Saved to output.md")
    
    print("\n" + "="*50)
    
    # 3. Custom configuration
    print("⚙️  Custom Configuration:")
    config = IngestConfig(
        output_format=OutputFormat.MARKDOWN,
        extract_images=False,
        extract_tables=True
    )
    
    ingestor = OpenIngestor(config=config)
    result = ingestor.ingest("documents/sample.md")
    print(f"✅ Configured ingestion: {len(result.content)} chars")
    
    print("\n" + "="*50)
    
    # 4. Get chunks for RAG
    print("🧩 Chunking for RAG:")
    chunks = result.get_chunks(chunk_size=500, overlap=50)
    print(f"📦 Split into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:2]):  # Show first 2
        print(f"  Chunk {i+1}: {len(chunk)} chars - {chunk[:100]}...")

def advanced_examples():
    """Advanced usage patterns"""
    
    print("📁 Directory Ingestion:")
    ingestor = OpenIngestor()
    
    # Ingest all supported files in directory
    results = ingestor.ingest_directory("documents/", "*.md")
    print(f"📊 Ingested {len(results)} documents")
    
    for result in results:
        print(f"  ✅ {result.filename}: {result.page_count} pages, {result.processing_time:.2f}s")
    
    print("\n" + "="*50)
    
    # 5. Ingest from bytes
    print("💾 Ingest from bytes:")
    with open("documents/sample.md", "rb") as f:
        file_bytes = f.read()
    
    result = ingestor.ingest_from_bytes(file_bytes, "sample.md")
    print(f"✅ Ingested {len(file_bytes)} bytes")
    print(f"📝 Content length: {len(result.content)}")

def rag_integration_example():
    """Example RAG pipeline integration"""
    
    print("🤖 RAG Pipeline Integration:")
    
    class SimpleRAG:
        def __init__(self):
            self.ingestor = OpenIngestor()
            self.documents = []
        
        def add_document(self, doc_path):
            result = self.ingestor.ingest(doc_path)
            chunks = result.get_chunks(chunk_size=800, overlap=100)
            
            for chunk in chunks:
                self.documents.append({
                    "content": chunk,
                    "source": result.filename,
                    "metadata": result.to_dict()
                })
            
            return len(chunks)
    
    # Use the RAG system
    rag = SimpleRAG()
    chunks_added = rag.add_document("documents/sample.md")
    print(f"📦 Added {chunks_added} chunks to RAG system")
    print(f"📊 Total documents in RAG: {len(rag.documents)}")

if __name__ == "__main__":
    main()
    print("\n" + "="*60)
    advanced_examples()
    print("\n" + "="*60)
    rag_integration_example()