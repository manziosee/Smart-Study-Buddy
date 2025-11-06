#!/usr/bin/env python3
"""
Simple API testing script for Smart Study Buddy
Run this after setting up the project to test basic functionality
"""

import requests
import json
import os

BASE_URL = "http://127.0.0.1:8000"

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 201:
        print("✅ Registration successful")
        return True
    else:
        print(f"❌ Registration failed: {response.text}")
        return False

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login successful")
        return response.cookies
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_text_summarization(cookies):
    """Test text summarization"""
    print("Testing text summarization...")
    
    data = {
        "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term 'artificial intelligence' is often used to describe machines that mimic 'cognitive' functions that humans associate with the human mind, such as 'learning' and 'problem solving'.",
        "method": "huggingface"
    }
    
    response = requests.post(f"{BASE_URL}/api/summarize/", json=data, cookies=cookies)
    print(f"Summarization: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Summarization successful")
        print(f"Summary: {result.get('summary', 'No summary returned')}")
        return True
    else:
        print(f"❌ Summarization failed: {response.text}")
        return False

def test_note_creation(cookies):
    """Test note creation"""
    print("Testing note creation...")
    
    data = {
        "title": "Test Note",
        "original_text": "This is a test note for the Smart Study Buddy application. It contains some sample text that can be used for testing summarization and quiz generation features."
    }
    
    response = requests.post(f"{BASE_URL}/api/notes/", json=data, cookies=cookies)
    print(f"Note creation: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print("✅ Note creation successful")
        return result['id']
    else:
        print(f"❌ Note creation failed: {response.text}")
        return None

def test_quiz_generation(note_id, cookies):
    """Test quiz generation"""
    print("Testing quiz generation...")
    
    data = {
        "note_id": note_id,
        "num_questions": 3,
        "method": "simple"  # Use simple method to avoid model loading issues
    }
    
    response = requests.post(f"{BASE_URL}/api/quiz/generate/", json=data, cookies=cookies)
    print(f"Quiz generation: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print("✅ Quiz generation successful")
        print(f"Generated {len(result.get('questions', []))} questions")
        return result['id']
    else:
        print(f"❌ Quiz generation failed: {response.text}")
        return None

def main():
    """Run all tests"""
    print("🧠 Smart Study Buddy API Test Suite")
    print("=" * 40)
    
    # Test registration
    if not test_registration():
        print("Skipping other tests due to registration failure")
        return
    
    # Test login
    cookies = test_login()
    if not cookies:
        print("Skipping other tests due to login failure")
        return
    
    # Test text summarization
    test_text_summarization(cookies)
    
    # Test note creation
    note_id = test_note_creation(cookies)
    if note_id:
        # Test quiz generation
        test_quiz_generation(note_id, cookies)
    
    print("\n🎉 API testing complete!")
    print("Check the Django admin at http://127.0.0.1:8000/admin/ to see created data")

if __name__ == "__main__":
    main()