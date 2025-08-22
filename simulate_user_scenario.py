#!/usr/bin/env python3
"""
Simulate the exact user scenario that was failing
"""

from conversion_optimization_agent import ConversionOptimizationAgent
from urllib.parse import urlparse

def simulate_user_scenario():
    print("🧪 Simulating Original User Scenario")
    print("=" * 45)
    
    agent = ConversionOptimizationAgent()
    
    # Simulate what happens in get_url_input with the problematic URL
    user_input = "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    
    print(f"User input: {user_input}")
    
    # Apply URL fixes (this was causing the problem)
    fixed_url = agent.fix_url_typos(user_input.strip())
    print(f"After fix_url_typos: {fixed_url}")
    
    # Add https if missing (this step wasn't the problem)
    if not fixed_url.startswith(('http://', 'https://')):
        fixed_url = 'https://' + fixed_url
        print(f"After adding https: {fixed_url}")
    
    # URL validation (this was failing before)
    try:
        parsed = urlparse(fixed_url)
        print(f"Parsed netloc: '{parsed.netloc}'")
        print(f"Parsed scheme: '{parsed.scheme}'")
        
        if parsed.netloc:
            agent.url = fixed_url
            print(f"✅ URL set: {agent.url}")
            
            # Test that scraping works
            success = agent.scrape_website()
            if success:
                print("✅ Scraping works!")
                return True
            else:
                print("❌ Scraping failed")
                return False
        else:
            print("❌ Invalid URL format - no netloc")
            return False
            
    except Exception as e:
        print(f"❌ URL parsing error: {e}")
        return False

if __name__ == "__main__":
    success = simulate_user_scenario()
    print(f"\n{'✅ FIXED' if success else '❌ STILL BROKEN'}: Original user scenario")