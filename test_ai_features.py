#!/usr/bin/env python3
"""Test AI features and endpoints"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api(endpoint, method="GET", data=None):
    """Test API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        print(f"\n{method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {json.dumps(result, indent=2)[:200]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Failed: {e}")

def main():
    print("🧪 Testing AI Features")
    
    # Test basic endpoints
    test_api("/api/notes/")
    test_api("/api/quizzes/")
    test_api("/api/analytics/")
    test_api("/api/dashboard/")
    test_api("/api/languages/")
    
    # Test with note ID 1 (if exists)
    test_api("/api/notes/1/analyze/", "POST")
    test_api("/api/notes/1/recommendations/")
    test_api("/api/notes/1/translate/", "POST", {"language": "es"})
    
    # Test quiz generation
    test_api("/api/quiz/generate/", "POST", {
        "note_id": 1,
        "num_questions": 3,
        "method": "groq"
    })
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    main()