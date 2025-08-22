#!/bin/bash

# Simple Document Export Setup Script
# Avoids problematic dependencies like WeasyPrint

echo "🚀 Setting up Simple Document Export for Testing Frameworks"
echo "=========================================================="

# Install only the reliable packages
echo "📦 Installing reliable packages..."

# Word document support (usually works fine)
echo "Installing Word document support..."
pip3 install python-docx

echo "✅ Setup complete!"

# Create the simple converter script
echo "📝 Creating simple converter script..."

cat > simple_convert_framework.py << 'EOF'
#!/usr/bin/env python3
"""
Simple Testing Framework Converter
Converts markdown to Word and beautiful HTML (Google Docs friendly)
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append('.')

try:
    from simple_document_exporter import SimpleDocumentExporter
except ImportError:
    print("❌ SimpleDocumentExporter not found. Make sure simple_document_exporter.py is in the same directory.")
    sys.exit(1)

def convert_framework(client_name, input_file, format_type='both'):
    """Convert framework file to specified format"""
    
    # Check input file
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    # Read markdown content
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Initialize exporter
    exporter = SimpleDocumentExporter(client_name)
    
    print(f"🔄 Converting {input_file} for {client_name}...")
    
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
                print(f"1. Open the HTML file in your browser")
                print(f"2. Select all content (Cmd+A)")
                print(f"3. Copy (Cmd+C)")
                print(f"4. Paste into Google Docs (Cmd+V)")
                print(f"5. Formatting will be preserved!")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 simple_convert_framework.py <client_name> <input_file.md> [format]")
        print("Formats: word, html, both (default)")
        print("")
        print("Examples:")
        print("  python3 simple_convert_framework.py \"Reality Events\" reality_events_framework.md")
        print("  python3 simple_convert_framework.py \"Reality Events\" reality_events_framework.md html")
        sys.exit(1)
    
    client_name = sys.argv[1]
    input_file = sys.argv[2]
    format_type = sys.argv[3] if len(sys.argv) > 3 else 'both'
    
    convert_framework(client_name, input_file, format_type)
EOF

chmod +x simple_convert_framework.py

echo "✅ Simple converter created: simple_convert_framework.py"

# Create directories
echo "📁 Creating export directories..."
mkdir -p exports/html
mkdir -p exports/word

echo ""
echo "🎯 Simple Usage Examples:"
echo ""
echo "# Convert to both Word and HTML (recommended)"
echo "python3 simple_convert_framework.py \"Reality Events\" reality_events_framework.md"
echo ""
echo "# Convert to HTML only (best for Google Docs)"
echo "python3 simple_convert_framework.py \"Reality Events\" reality_events_framework.md html"
echo ""
echo "# Convert to Word only"
echo "python3 simple_convert_framework.py \"Reality Events\" reality_events_framework.md word"
echo ""
echo "🚀 Setup complete! No complex dependencies required."
echo ""
echo "💡 For Google Docs workflow:"
echo "1. Generate HTML version"
echo "2. Open HTML file in browser"
echo "3. Copy all content (Cmd+A, Cmd+C)"
echo "4. Paste into Google Docs (Cmd+V)"
echo "5. Perfect formatting preserved!"