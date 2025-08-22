#!/usr/bin/env python3
"""
Fixed Simple Testing Framework Converter
Handles spaces in client names and file paths properly
"""

import sys
import os
import re
from pathlib import Path

# Add current directory to path
sys.path.append('.')

try:
    from simple_document_exporter import SimpleDocumentExporter
except ImportError:
    print("❌ SimpleDocumentExporter not found. Make sure simple_document_exporter.py is in the same directory.")
    sys.exit(1)

class FixedSimpleDocumentExporter(SimpleDocumentExporter):
    def __init__(self, client_name: str, project_path: str = None):
        self.client_name = client_name
        # Create a safe directory name (no spaces or special characters)
        safe_name = re.sub(r'[^\w\-_]', '_', client_name.lower())
        
        # Use current directory for exports instead of client-specific directory
        self.project_path = Path('.')
        self.output_dir = self.project_path / "exports" / safe_name
        
        # Create the directory safely
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # Fallback to simple exports directory
            self.output_dir = Path('./exports')
            self.output_dir.mkdir(exist_ok=True)
            print(f"⚠️  Using fallback directory: {self.output_dir}")

def convert_framework(client_name, input_file, format_type='both'):
    """Convert framework file to specified format"""
    
    # Check input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    # Read markdown content
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # Initialize exporter with fixed version
    exporter = FixedSimpleDocumentExporter(client_name)
    
    print(f"🔄 Converting {input_path.name} for {client_name}...")
    print(f"📁 Output directory: {exporter.output_dir}")
    
    try:
        if format_type == 'word':
            word_path = exporter.export_to_word(content)
            if word_path:
                print(f"✅ Word: {word_path}")
        
        elif format_type == 'html':
            html_path = exporter.export_to_html(content)
            print(f"✅ HTML: {html_path}")
            print(f"💡 Open the HTML file in your browser, then copy/paste to Google Docs")
        
        else:  # both
            results = exporter.export_both_formats(content)
            for format_name, result in results.items():
                if 'error' in format_name:
                    print(f"❌ {format_name}: {result}")
                elif 'info' in format_name:
                    print(f"💡 {format_name}: {result}")
                else:
                    print(f"✅ {format_name}: {result}")
            
            if 'html' in results:
                print(f"\n🎯 Best workflow for Google Docs:")
                print(f"1. Open the HTML file in your browser: {results['html']}")
                print(f"2. Select all content (Cmd+A)")
                print(f"3. Copy (Cmd+C)")
                print(f"4. Paste into Google Docs (Cmd+V)")
                print(f"5. Formatting will be preserved!")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function with better error handling"""
    if len(sys.argv) < 3:
        print("Usage: python3 fixed_simple_converter.py <client_name> <input_file.md> [format]")
        print("Formats: word, html, both (default)")
        print("")
        print("Examples:")
        print('  python3 fixed_simple_converter.py "Reality Events" reality_events_framework.md')
        print('  python3 fixed_simple_converter.py "Reality Events" reality_events_framework.md html')
        print('  python3 fixed_simple_converter.py "Reality Events" "/full/path/to/file.md"')
        return
    
    client_name = sys.argv[1]
    input_file = sys.argv[2]
    format_type = sys.argv[3] if len(sys.argv) > 3 else 'both'
    
    # Validate format
    if format_type not in ['word', 'html', 'both']:
        print(f"❌ Invalid format: {format_type}")
        print("Valid formats: word, html, both")
        return
    
    print(f"🚀 Starting conversion...")
    print(f"📝 Client: {client_name}")
    print(f"📄 Input: {input_file}")
    print(f"🎯 Format: {format_type}")
    print()
    
    convert_framework(client_name, input_file, format_type)

if __name__ == "__main__":
    main()