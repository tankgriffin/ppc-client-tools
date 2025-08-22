#!/usr/bin/env python3
"""
Test the actual agent's fixed URL correction
"""

from conversion_optimization_agent import ConversionOptimizationAgent

def test_real_fix():
    print("🧪 Testing Real Fixed URL Correction")
    print("=" * 45)
    
    agent = ConversionOptimizationAgent()
    
    # Test cases
    test_cases = [
        "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/",  # Valid - should NOT change
        "ttps://example.com",   # Missing h - should fix
        "https:/example.com",   # Missing slash after colon - should fix  
        "https//example.com"    # Missing colon - should fix
    ]
    
    for i, test_url in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_url}")
        original_length = len(test_url)
        corrected = agent.fix_url_typos(test_url)
        corrected_length = len(corrected)
        
        print(f"Result:  {corrected}")
        print(f"Changed: {test_url != corrected}")
        print(f"Length:  {original_length} → {corrected_length}")
        
        if test_url == corrected:
            print("✅ URL unchanged (correct)")
        else:
            print(f"🔄 URL modified")

if __name__ == "__main__":
    test_real_fix()