#!/usr/bin/env python
import requests
import sys

def test_url(url, name):
    try:
        response = requests.get(url, timeout=10)
        print(f"{name}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text[:200]}")
        return response.status_code == 200
    except Exception as e:
        print(f"{name}: ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    base_url = "http://localhost:8000"
    
    print("Testing Campus Shoppy URLs...")
    print("=" * 40)
    
    urls_to_test = [
        ("/", "Homepage"),
        ("/shop/", "Shop"),
        ("/blog/", "Blog"),
        ("/health/", "Health Check"),
        ("/about/", "About"),
        ("/contact/", "Contact"),
    ]
    
    results = []
    for url, name in urls_to_test:
        full_url = base_url + url
        success = test_url(full_url, name)
        results.append((name, success))
    
    print("\n" + "=" * 40)
    print("SUMMARY:")
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
