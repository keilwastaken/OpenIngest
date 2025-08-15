#!/usr/bin/env python3
"""
OpenIngest CLI - Simple document ingestion
"""

import sys
import argparse
from pathlib import Path
from .ingestor import OpenIngestor
from .models import IngestConfig, OutputFormat

def main():
    parser = argparse.ArgumentParser(
        description="OpenIngest - Open-source document ingestion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  openingest document.pdf                    # Quick ingest to stdout
  openingest document.pdf -o output.md      # Save to file
  openingest docs/ -o processed/             # Process directory
  openingest document.pdf --format json     # Output as JSON
        """
    )
    
    parser.add_argument("input", help="Document file or directory to process")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("--format", choices=["markdown", "html", "json", "text"], 
                       default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Create config
    format_map = {
        "markdown": OutputFormat.MARKDOWN,
        "html": OutputFormat.HTML, 
        "json": OutputFormat.JSON,
        "text": OutputFormat.TEXT
    }
    
    config = IngestConfig(output_format=format_map[args.format])
    ingestor = OpenIngestor(config)
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: {input_path} does not exist", file=sys.stderr)
        sys.exit(1)
    
    try:
        if input_path.is_file():
            # Process single file
            if args.verbose:
                print(f"Processing {input_path}...", file=sys.stderr)
            
            result = ingestor.ingest(str(input_path))
            
            if args.output:
                result.save(args.output)
                if args.verbose:
                    print(f"Saved to {args.output}", file=sys.stderr)
            else:
                print(result.content)
                
        elif input_path.is_dir():
            # Process directory
            if args.verbose:
                print(f"Processing directory {input_path}...", file=sys.stderr)
            
            results = ingestor.ingest_directory(str(input_path))
            
            if args.output:
                output_dir = Path(args.output)
                output_dir.mkdir(exist_ok=True)
                
                for result in results:
                    output_file = output_dir / f"{Path(result.filename).stem}.md"
                    result.save(str(output_file))
                    if args.verbose:
                        print(f"Saved {result.filename} to {output_file}", file=sys.stderr)
            else:
                for result in results:
                    print(f"\n=== {result.filename} ===")
                    print(result.content)
                    
        if args.verbose:
            print("Processing complete!", file=sys.stderr)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()