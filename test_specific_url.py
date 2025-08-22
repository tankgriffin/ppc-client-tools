#!/usr/bin/env python3
"""
Test the specific URL that was causing the 403 error
"""

from conversion_optimization_agent import ConversionOptimizationAgent

def test_specific_url():
    print("🧪 Testing Specific URL")
    print("=" * 40)
    
    # Create agent instance
    agent = ConversionOptimizationAgent()
    
    # Set the problematic URL
    test_url = "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
    agent.url = test_url
    print(f"Testing URL: {agent.url}")
    
    # Test scraping with improved method
    success = agent.scrape_website()
    
    if success:
        print("\n✅ Successfully scraped the website!")
        print(f"Found {len(agent.soup.find_all('p'))} paragraphs")
        print(f"Found {len(agent.soup.find_all('h1'))} H1 tags")
        print(f"Found {len(agent.soup.find_all('img'))} images")
        return True
    else:
        print("\n❌ Failed to scrape the website")
        return False

if __name__ == "__main__":
    test_specific_url()