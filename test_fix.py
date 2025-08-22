#!/usr/bin/env python3
"""
Test the fixed URL correction
"""

from conversion_optimization_agent import ConversionOptimizationAgent

def test_url_fix():
    print("🧪 Testing Fixed URL Correction")
    print("=" * 40)
    
    agent = ConversionOptimizationAgent()
    
    # Test cases
    test_cases = [
        "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/",  # Valid URL - should NOT change
        "ttps://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/",   # Typo - should fix
        "https//example.com",  # Missing colon - should fix
        "https://example.com//path//to//page"  # Double slashes in path - should fix
    ]
    
    for i, test_url in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_url}")
        corrected = agent.fix_url_typos(test_url)
        print(f"Result:  {corrected}")
        
        # Test that it parses correctly
        from urllib.parse import urlparse
        try:
            parsed = urlparse(corrected)
            if parsed.netloc:
                print("✅ Valid URL format")
            else:
                print("❌ Invalid URL format")
        except Exception as e:
            print(f"❌ Parse error: {e}")
    
    print(f"\n{'='*40}")
    print("Testing the specific problematic case:")
    problematic_url = "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    fixed = agent.fix_url_typos(problematic_url)
    print(f"Input:  {problematic_url}")
    print(f"Output: {fixed}")
    print(f"Same?   {problematic_url == fixed}")

if __name__ == "__main__":
    test_url_fix()