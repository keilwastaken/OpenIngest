"""
Side-by-side comparison: OpenIngest vs LlamaParse
Same API design, but self-hosted and private
"""

def llamaparse_style():
    """How you would use LlamaParse (for comparison)"""
    print("📄 LlamaParse Style (cloud-based):")
    
    # This is how LlamaParse works:
    """
    from llama_parse import LlamaParse
    
    parser = LlamaParse(
        api_key="llx-...",  # Required API key
        result_type="markdown"
    )
    
    documents = parser.load_data("document.pdf")
    content = documents[0].text
    """
    
    print("❌ Requires API key and sends data to cloud")
    print("💳 Costs money per page")
    print("🌐 Depends on internet connection")

def openingest_style():
    """How you use OpenIngest (our alternative)"""
    print("🚀 OpenIngest Style (self-hosted):")
    
    from openingest import OpenIngestor, IngestConfig, OutputFormat
    
    # Same simplicity, but self-hosted
    ingestor = OpenIngestor(IngestConfig(
        output_format=OutputFormat.MARKDOWN
    ))
    
    result = ingestor.ingest("../sample.md")
    content = result.content
    
    print("✅ No API key needed")
    print("🔒 Data stays on your infrastructure") 
    print("💰 No per-page costs")
    print("⚡ No internet dependency")
    print(f"📄 Ingested: {result.filename}")
    print(f"📊 Content: {len(content)} characters")

def api_comparison():
    """Direct API comparison"""
    
    print("\n🔄 API Comparison:")
    print("="*50)
    
    print("LlamaParse:")
    print("```python")
    print("from llama_parse import LlamaParse")
    print("parser = LlamaParse(api_key='llx-...')")
    print("docs = parser.load_data('file.pdf')")
    print("content = docs[0].text")
    print("```")
    
    print("\nOpenIngest:")
    print("```python") 
    print("from openingest import OpenIngestor")
    print("ingestor = OpenIngestor()")
    print("result = ingestor.ingest('file.pdf')")
    print("content = result.content")
    print("```")
    
    print("\n📊 Feature Comparison:")
    features = [
        ("API Simplicity", "✅ Simple", "✅ Simple"),
        ("Setup", "❌ Need API key", "✅ Just import"),
        ("Privacy", "❌ Data sent to cloud", "✅ Data stays local"),
        ("Cost", "💳 Per-page pricing", "💰 Infrastructure only"),
        ("Offline", "❌ Requires internet", "✅ Works offline"),
        ("Customization", "❌ Limited", "✅ Full control"),
        ("Formats", "📄 Mainly PDF", "📄 PDF, DOCX, PPTX, etc."),
    ]
    
    print(f"{'Feature':<15} | {'LlamaParse':<20} | {'OpenIngest'}")
    print("-" * 60)
    for feature, llama, open_ing in features:
        print(f"{feature:<15} | {llama:<20} | {open_ing}")

def migration_example():
    """How to migrate from LlamaParse to OpenIngest"""
    
    print("\n🔄 Migration Example:")
    print("="*30)
    
    print("Before (LlamaParse):")
    print("```python")
    print("from llama_parse import LlamaParse")
    print("")
    print("parser = LlamaParse(")
    print("    api_key='your-api-key',")
    print("    result_type='markdown'")
    print(")")
    print("")
    print("documents = parser.load_data('research.pdf')")
    print("for doc in documents:")
    print("    print(doc.text)")
    print("```")
    
    print("\nAfter (OpenIngest):")
    print("```python")
    print("from openingest import OpenIngestor, IngestConfig, OutputFormat")
    print("")
    print("ingestor = OpenIngestor(IngestConfig(")
    print("    output_format=OutputFormat.MARKDOWN")
    print("))")
    print("")
    print("result = ingestor.ingest('research.pdf')")
    print("print(result.content)")
    print("```")
    
    print("\n✅ Migration benefits:")
    print("- Remove API key dependency")
    print("- Eliminate per-page costs")
    print("- Keep data private")
    print("- Work offline")
    print("- Same simple API!")

if __name__ == "__main__":
    llamaparse_style()
    print("\n" + "="*60)
    openingest_style()
    print("\n" + "="*60)
    api_comparison()
    migration_example()