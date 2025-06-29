#!/usr/bin/env python3
"""
Quick Setup Script - Simplified version for testing
"""

import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 quick_setup.py 'Client Name'")
        sys.exit(1)
    
    client_name = sys.argv[1]
    
    print(f"🚀 Quick Setup for {client_name}")
    print("=" * 50)
    
    # Step 1: Create project structure
    print("\n📁 Step 1: Creating project structure...")
    try:
        result = subprocess.run(['./setup_client.sh', client_name], check=True)
        print("✅ Project structure created")
    except subprocess.CalledProcessError:
        print("❌ Failed to create project structure")
        sys.exit(1)
    
    # Step 2: Run Claude research setup
    print(f"\n🧠 Step 2: Running Claude AI research setup...")
    print("This will ask you questions about the business...")
    try:
        result = subprocess.run(['python3', 'claude_research_setup.py', client_name], check=True)
        print("✅ Claude research setup completed")
    except subprocess.CalledProcessError:
        print("❌ Claude research setup failed")
        sys.exit(1)
    
    # Step 3: Show next steps
    client_folder = client_name.lower().replace(' ', '_')
    print(f"\n🎉 Setup completed successfully!")
    print(f"\n📁 Your files are in: {client_folder}/")
    print(f"🧠 Claude research: {client_folder}/02_market_research/claude_research/")
    print(f"\n📋 Next steps:")
    print(f"1. cd {client_folder}/02_market_research/claude_research/")
    print(f"2. Open CLAUDE_RESEARCH_SUMMARY.md")
    print(f"3. Execute the 5 research phases in Claude AI")
    print(f"4. Save Claude's responses in phase_outputs/ folder")

if __name__ == "__main__":
    main()