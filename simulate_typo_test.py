#!/usr/bin/env python3
"""
Simulate the typo scenario and test the full workflow
"""

from conversion_optimization_agent import ConversionOptimizationAgent
import io
import sys

def simulate_user_input_with_typo():
    print("🧪 Simulating User Input with Typo")
    print("=" * 45)
    
    # Simulate the typo scenario
    agent = ConversionOptimizationAgent()
    
    # Test the fix_url_typos method directly
    typo_url = "ttps://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    fixed_url = agent.fix_url_typos(typo_url)
    
    print(f"Original (with typo): {typo_url}")
    print(f"Auto-corrected:       {fixed_url}")
    
    # Set the corrected URL and test full workflow
    agent.url = fixed_url
    
    print(f"\n🚀 Running full analysis with corrected URL...")
    
    # Test scraping
    if agent.scrape_website():
        print("✅ Scraping successful")
        
        # Run analyses
        cro_results = agent.analyze_cro_framework()
        seo_results = agent.analyze_seo_framework()
        
        # Generate report
        pdf_file = agent.generate_pdf_report()
        
        if pdf_file:
            print(f"\n✅ Complete workflow successful!")
            print(f"📄 Report generated: {pdf_file}")
            
            recommendations = agent.generate_recommendations()
            print(f"📊 Issues found: {len(recommendations['high_priority'])}")
            print(f"📈 Opportunities: {len(recommendations['medium_priority'])}")
            return True
    
    return False

if __name__ == "__main__":
    success = simulate_user_input_with_typo()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Typo correction and full workflow test")