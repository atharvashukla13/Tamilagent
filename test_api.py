# -*- coding: utf-8 -*-
"""
Test script for Tamil Agricultural Page Prediction API
"""

import requests
import json
import time

def test_api():
    """Test the Tamil Agricultural Page Prediction API"""
    
    base_url = "http://localhost:5000"
    
    print("Testing Tamil Agricultural Page Prediction API")
    print("=" * 60)
    
    # Test queries in Tamil
    test_queries = [
        "என்டிவிஐ மூலம் பயிர்களின் ஆரோக்கியத்தை மதிப்பிடலாம்",
        "விளைச்சல் முன்னறிவிப்பு",
        "பயிர்நோய் கண்டறிதல்",
        "நீர்ப்பாசனத் திட்டம்",
        "பயிர் பரிந்துரை"
    ]
    
    print("\n1. Testing Prediction Endpoint")
    print("-" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        try:
            response = requests.post(f"{base_url}/predict", 
                                  json={"query": query},
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
    
    print("\n\n2. Testing Statistics Endpoint")
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
    
    print("\n\n3. Testing Pages Endpoint")
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
    
    print("\n\n4. Testing Visualization Endpoint")
    print("-" * 40)
    
    try:
        response = requests.post(f"{base_url}/visualize/similarity", 
                              json={"query": "விளைச்சல் முன்னறிவிப்பு"},
                              timeout=15)
        if response.status_code == 200:
            data = response.json()
            if 'image' in data:
                print("[SUCCESS] Similarity visualization generated successfully")
                print(f"   Image data length: {len(data['image'])} characters")
            else:
                print("[ERROR] No image data in response")
        else:
            print(f"[ERROR] {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
    
    print("\n\n5. Testing GET Prediction Endpoint")
    print("-" * 40)
    
    try:
        query = "உரம் மற்றும் பூச்சிக்கொல்லி அறிவகம்"
        response = requests.get(f"{base_url}/predict", 
                              params={"query": query},
                              timeout=10)
        if response.status_code == 200:
            data = response.json()
            top_prediction = data.get('top_prediction', {})
            print("[SUCCESS] GET Prediction successful")
            print(f"   Query: {query}")
            print(f"   Predicted Page: {top_prediction.get('page_name', 'N/A')}")
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
    test_api()
