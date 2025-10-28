# -*- coding: utf-8 -*-
"""
Simple test script for Tamil Agricultural Page Prediction API
"""

import requests
import json

def test_api_simple():
    """Test the Tamil Agricultural Page Prediction API"""
    
    base_url = "http://localhost:5000"
    
    print("Testing Tamil Agricultural Page Prediction API")
    print("=" * 60)
    
    # Test a simple prediction
    test_query = "விளைச்சல் முன்னறிவிப்பு"  # Yield prediction
    
    print(f"\n1. Testing Prediction Endpoint")
    print("-" * 40)
    print("Query: Tamil text for yield prediction")
    
    try:
        response = requests.post(f"{base_url}/predict", 
                              json={"query": test_query},
                              timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            top_prediction = data.get('top_prediction', {})
            print(f"[SUCCESS] Predicted Page: {top_prediction.get('page_name', 'N/A')}")
            print(f"   Similarity Score: {top_prediction.get('similarity_score', 0):.4f}")
            print(f"   Description: {top_prediction.get('description', 'N/A')}")
        else:
            print(f"[ERROR] {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"[CONNECTION ERROR] {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
        return
    
    print(f"\n2. Testing Statistics Endpoint")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"[SUCCESS] Total Pages: {stats.get('total_pages', 0)}")
            print(f"[SUCCESS] Total Keywords: {stats.get('total_keywords', 0)}")
            print(f"[SUCCESS] Average Keywords per Page: {stats.get('avg_keywords_per_page', 0):.2f}")
        else:
            print(f"[ERROR] {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
    
    print(f"\n3. Testing Pages Endpoint")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/pages", timeout=10)
        if response.status_code == 200:
            data = response.json()
            pages = data.get('pages', [])
            print(f"[SUCCESS] Retrieved {len(pages)} pages")
            print("   Sample pages:")
            for page in pages[:3]:  # Show first 3 pages
                print(f"   - {page.get('page_name', 'N/A')}: {len(page.get('keywords', []))} keywords")
        else:
            print(f"[ERROR] {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
    
    print("\n" + "=" * 60)
    print("API Testing Complete!")
    print("\nTo start the Flask server, run:")
    print("python app.py")
    print("\nThen open your browser to:")
    print("http://localhost:5000")

if __name__ == "__main__":
    test_api_simple()