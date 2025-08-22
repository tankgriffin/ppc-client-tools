#!/usr/bin/env python3
"""
Test URL typo correction functionality
"""

from conversion_optimization_agent import ConversionOptimizationAgent

def test_url_fixes():
    print("🧪 Testing URL Typo Correction")
    print("=" * 40)
    
    agent = ConversionOptimizationAgent()
    
    # Test cases with common typos
    test_cases = [
        "ttps://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/",
        "htps://example.com",
        "htp://example.com",
        "https//example.com",
        "http//example.com", 
        "https:/example.com",
        "http:/example.com",
        "www.https://example.com",
        "www.http://example.com",
        "https://example.com//path//to//page"
    ]
    
    expected_results = [
        "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/",
        "https://example.com",
        "http://example.com",
        "https://example.com",
        "http://example.com",
        "https://example.com",
        "http://example.com",
        "https://www.example.com",
        "http://www.example.com",
        "https://example.com/path/to/page"
    ]
    
    print("Testing URL corrections:")
    for i, (test_url, expected) in enumerate(zip(test_cases, expected_results)):
        corrected = agent.fix_url_typos(test_url)
        status = "✅" if corrected == expected else "❌"
        print(f"{status} Test {i+1}:")
        print(f"   Input:    {test_url}")
        print(f"   Output:   {corrected}")
        print(f"   Expected: {expected}")
        if corrected != expected:
            print(f"   ⚠️ MISMATCH!")
        print()
    
    # Test the specific problematic URL
    print("Testing the specific problematic URL:")
    problematic_url = "ttps://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    corrected = agent.fix_url_typos(problematic_url)
    print(f"Input:  {problematic_url}")
    print(f"Fixed:  {corrected}")
    
    # Test that it actually works by trying to set it
    agent.url = corrected
    success = agent.scrape_website()
    
    if success:
        print("✅ Successfully scraped the corrected URL!")
    else:
        print("❌ Still failed to scrape")

if __name__ == "__main__":
    test_url_fixes()