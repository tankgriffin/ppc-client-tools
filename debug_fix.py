#!/usr/bin/env python3
"""
Debug the URL correction issue
"""

def debug_url_fix(url):
    print(f"Debugging URL: {url}")
    
    protocol_fixes = {
        'ttps://': 'https://',
        'htps://': 'https://',
        'htp://': 'http://',
        'https//': 'https://',
        'http//': 'http://',
        'https:/': 'https://',
        'http:/': 'http://',
        'www.https://': 'https://www.',
        'www.http://': 'http://www.'
    }
    
    print(f"Original URL: '{url}'")
    
    for typo, correct in protocol_fixes.items():
        if url.startswith(typo):
            print(f"FOUND MATCH: '{typo}' → '{correct}'")
            corrected = url.replace(typo, correct, 1)
            print(f"After replacement: '{corrected}'")
            return corrected
        else:
            print(f"No match for: '{typo}'")
    
    print("No corrections applied")
    return url

# Test the problematic URL
test_url = "https://theloungeaesthetics.com.au/injectables/volume-and-define/jowls/"
result = debug_url_fix(test_url)
print(f"\nFinal result: '{result}'")
print(f"Same as input? {result == test_url}")
print(f"Length difference: {len(result) - len(test_url)}")

if result != test_url:
    print("Character comparison:")
    for i, (a, b) in enumerate(zip(test_url, result)):
        if a != b:
            print(f"  Position {i}: '{a}' → '{b}'")
    if len(result) > len(test_url):
        print(f"  Extra characters: '{result[len(test_url):]}'")
    elif len(test_url) > len(result):
        print(f"  Missing characters: '{test_url[len(result):]}'")