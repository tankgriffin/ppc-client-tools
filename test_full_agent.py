#!/usr/bin/env python3
"""
Test the full agent with the previously problematic URL
"""

from conversion_optimization_agent import ConversionOptimizationAgent

def test_full_agent():
    print("🧪 Testing Full Agent with Real URL")
    print("=" * 45)
    
    # Create agent instance
    agent = ConversionOptimizationAgent()
    
    # Set the URL that was previously failing
    test_url = "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    agent.url = test_url
    print(f"Testing URL: {agent.url}")
    
    # Run full analysis
    if agent.scrape_website():
        print("\n📊 Running full analysis...")
        
        # Run CRO analysis
        cro_results = agent.analyze_cro_framework()
        print(f"✅ CRO Analysis completed - {len(cro_results)} sections analyzed")
        
        # Run SEO analysis  
        seo_results = agent.analyze_seo_framework()
        print(f"✅ SEO Analysis completed - {len(seo_results)} sections analyzed")
        
        # Generate PDF report
        pdf_file = agent.generate_pdf_report()
        
        if pdf_file:
            print(f"\n✅ Full test successful! Report: {pdf_file}")
            
            # Show summary
            recommendations = agent.generate_recommendations()
            print(f"\n📋 Analysis Summary:")
            print(f"• High priority issues: {len(recommendations['high_priority'])}")
            print(f"• Medium priority recommendations: {len(recommendations['medium_priority'])}")
            
            # Show some specific findings
            if recommendations['high_priority']:
                print(f"\n🔴 Top issues found:")
                for i, issue in enumerate(recommendations['high_priority'][:3], 1):
                    print(f"  {i}. {issue}")
                    
            return True
        else:
            print("❌ PDF generation failed")
            return False
    else:
        print("❌ Website scraping failed")
        return False

if __name__ == "__main__":
    test_full_agent()