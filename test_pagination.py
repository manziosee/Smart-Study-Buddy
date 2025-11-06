#!/usr/bin/env python3
"""
Quick test script for pagination and filtering features
Run: python3 test_pagination.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint, params=None):
    """Test an API endpoint with optional parameters"""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params)
        print(f"\n{'='*60}")
        print(f"Testing: {endpoint}")
        if params:
            print(f"Params: {params}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                print(f"Total items: {data.get('count', 'N/A')}")
                print(f"Current page: {data.get('current_page', 'N/A')}")
                print(f"Total pages: {data.get('total_pages', 'N/A')}")
                print(f"Items on page: {len(data['results'])}")
                print(f"Has next: {bool(data['links']['next'])}")
                print(f"Has previous: {bool(data['links']['previous'])}")
            else:
                print(f"Response: {json.dumps(data, indent=2)[:200]}...")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Server not running at {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    print("🧪 Testing Smart Study Buddy API Pagination & Filtering")
    
    # Test basic pagination
    if not test_endpoint("/api/notes/"):
        print("\n❌ Server not accessible. Start with: python3 manage.py runserver")
        return
    
    # Test pagination parameters
    test_endpoint("/api/notes/", {"page": 2, "page_size": 5})
    
    # Test search
    test_endpoint("/api/notes/", {"search": "python"})
    
    # Test filtering
    test_endpoint("/api/notes/", {"has_summary": "true"})
    test_endpoint("/api/notes/", {"title": "test"})
    
    # Test sorting
    test_endpoint("/api/notes/", {"ordering": "-created_at"})
    test_endpoint("/api/notes/", {"ordering": "title"})
    
    # Test combined parameters
    test_endpoint("/api/notes/", {
        "search": "test",
        "page_size": 10,
        "ordering": "-created_at"
    })
    
    # Test quizzes
    test_endpoint("/api/quizzes/")
    test_endpoint("/api/quizzes/", {"page_size": 5})
    
    # Test quiz attempts
    test_endpoint("/api/quiz/attempts/")
    
    print(f"\n{'='*60}")
    print("✅ Testing complete!")
    print("📖 Check Swagger docs at: http://127.0.0.1:8000/api/docs/")

if __name__ == "__main__":
    main()