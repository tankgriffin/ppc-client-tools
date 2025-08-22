#!/usr/bin/env python3
"""
Demo test for the Conversion Optimization Agent
This simulates user input for testing purposes
"""

from conversion_optimization_agent import ConversionOptimizationAgent
import sys

def demo_test():
    print("🧪 Running Demo Test of Conversion Optimization Agent")
    print("=" * 60)
    
    # Create agent instance
    agent = ConversionOptimizationAgent()
    
    # Set a test URL directly (simulating user input)
    test_url = "https://example.com"
    agent.url = test_url
    print(f"✅ Using test URL: {agent.url}")
    
    # Test scraping
    if not agent.scrape_website():
        print("❌ Failed to scrape website")
        return False
    
    # Run analyses
    print("\n📊 Running CRO Analysis...")
    cro_results = agent.analyze_cro_framework()
    print(f"✅ CRO Analysis completed - {len(cro_results)} sections analyzed")
    
    print("\n🔍 Running SEO Analysis...")
    seo_results = agent.analyze_seo_framework()
    print(f"✅ SEO Analysis completed - {len(seo_results)} sections analyzed")
    
    # Generate report
    print("\n📄 Generating PDF Report...")
    pdf_file = agent.generate_pdf_report()
    
    if pdf_file:
        print(f"✅ Demo test successful! Report generated: {pdf_file}")
        
        # Show summary
        recommendations = agent.generate_recommendations()
        print(f"\n📋 Demo Results Summary:")
        print(f"• High priority issues: {len(recommendations['high_priority'])}")
        print(f"• Medium priority recommendations: {len(recommendations['medium_priority'])}")
        print(f"• PDF report: {pdf_file}")
        
        return True
    else:
        print("❌ Demo test failed - PDF generation error")
        return False

if __name__ == "__main__":
    success = demo_test()
    sys.exit(0 if success else 1)