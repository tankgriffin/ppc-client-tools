#!/usr/bin/env python3
"""
Command-line version of the Conversion Optimization Agent
Usage: python3 analyze_url.py <URL>
"""

import sys
from conversion_optimization_agent import ConversionOptimizationAgent

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_url.py <URL>")
        print("Example: python3 analyze_url.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Create and run agent
    agent = ConversionOptimizationAgent()
    agent.url = url
    
    print(f"🚀 Analyzing: {url}")
    print("=" * 60)
    
    # Run analysis
    if agent.scrape_website():
        agent.analyze_cro_framework()
        agent.analyze_seo_framework()
        
        pdf_file = agent.generate_pdf_report()
        
        if pdf_file:
            print(f"\n✅ Analysis complete! Report: {pdf_file}")
            recommendations = agent.generate_recommendations()
            print(f"📊 Found {len(recommendations['high_priority'])} critical issues")
            print(f"📈 Found {len(recommendations['medium_priority'])} optimization opportunities")
        else:
            print("❌ Failed to generate report")
            sys.exit(1)
    else:
        print("❌ Failed to analyze website")
        sys.exit(1)

if __name__ == "__main__":
    main()