#!/usr/bin/env python3
"""
Test the complete workflow with the fixed URL
"""

from conversion_optimization_agent import ConversionOptimizationAgent

def test_complete_workflow():
    print("🧪 Testing Complete Workflow")
    print("=" * 40)
    
    agent = ConversionOptimizationAgent()
    
    # Test with the exact URL that was causing problems
    test_url = "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    print(f"Testing URL: {test_url}")
    
    # Fix URL (should be unchanged now)
    fixed_url = agent.fix_url_typos(test_url)
    print(f"After URL fix: {fixed_url}")
    print(f"URLs match: {test_url == fixed_url}")
    
    # Set the URL and run full analysis
    agent.url = fixed_url
    
    print("\n🚀 Running complete analysis...")
    
    if agent.scrape_website():
        print("✅ Scraping successful")
        
        # Run analyses
        cro_results = agent.analyze_cro_framework()
        seo_results = agent.analyze_seo_framework()
        
        # Generate PDF
        pdf_file = agent.generate_pdf_report()
        
        if pdf_file:
            print(f"✅ Complete workflow successful!")
            print(f"📄 Report: {pdf_file}")
            
            recommendations = agent.generate_recommendations()
            print(f"📊 Issues: {len(recommendations['high_priority'])}")
            print(f"📈 Opportunities: {len(recommendations['medium_priority'])}")
            
            return True
        else:
            print("❌ PDF generation failed")
    else:
        print("❌ Scraping failed")
    
    return False

if __name__ == "__main__":
    success = test_complete_workflow()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Complete workflow test")