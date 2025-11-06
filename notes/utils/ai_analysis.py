import requests
from django.conf import settings
import json
import re


def analyze_content_with_groq(text):
    """Analyze content to extract key concepts, topics, and themes using Groq"""
    api_key = settings.GROQ_API_KEY
    if not api_key or api_key == 'your_groq_key_here':
        return extract_basic_concepts(text)
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messages': [
                {
                    'role': 'system',
                    'content': '''You are an expert content analyzer. Analyze the given text and return a JSON response with:
                    {
                        "key_concepts": ["concept1", "concept2", ...],
                        "main_topics": ["topic1", "topic2", ...],
                        "difficulty_level": "beginner|intermediate|advanced",
                        "estimated_read_time": "X minutes",
                        "subject_area": "subject name"
                    }'''
                },
                {
                    'role': 'user',
                    'content': f'Analyze this text: {text[:2000]}'  # Limit text length
                }
            ],
            'model': 'llama3-8b-8192',
            'temperature': 0.2,
            'max_tokens': 300
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            # Try to parse JSON response
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Extract information from text response
                return parse_analysis_text(content)
        else:
            return extract_basic_concepts(text)
            
    except Exception as e:
        return extract_basic_concepts(text)


def extract_basic_concepts(text):
    """Basic concept extraction without AI"""
    words = re.findall(r'\b[A-Z][a-z]+\b', text)
    concepts = list(set(words))[:10]
    
    word_count = len(text.split())
    read_time = max(1, word_count // 200)
    
    return {
        'key_concepts': concepts,
        'main_topics': concepts[:5],
        'difficulty_level': 'intermediate',
        'estimated_read_time': f'{read_time} minutes',
        'subject_area': 'General'
    }


def parse_analysis_text(text):
    """Parse analysis from text response"""
    try:
        concepts = re.findall(r'concept[s]?[:\-]\s*(.+)', text, re.IGNORECASE)
        topics = re.findall(r'topic[s]?[:\-]\s*(.+)', text, re.IGNORECASE)
        difficulty = re.findall(r'difficulty[:\-]\s*(\w+)', text, re.IGNORECASE)
        
        return {
            'key_concepts': concepts[0].split(',')[:5] if concepts else [],
            'main_topics': topics[0].split(',')[:3] if topics else [],
            'difficulty_level': difficulty[0] if difficulty else 'intermediate',
            'estimated_read_time': '5 minutes',
            'subject_area': 'General'
        }
    except:
        return extract_basic_concepts(text)


def generate_study_recommendations(analysis, user_history=None):
    """Generate personalized study recommendations based on content analysis"""
    recommendations = []
    
    difficulty = analysis.get('difficulty_level', 'intermediate')
    concepts = analysis.get('key_concepts', [])
    
    if difficulty == 'beginner':
        recommendations.append("Start with basic concepts and definitions")
        recommendations.append("Use flashcards for key terms")
    elif difficulty == 'advanced':
        recommendations.append("Focus on connecting complex concepts")
        recommendations.append("Create detailed mind maps")
    else:
        recommendations.append("Practice with quiz questions")
        recommendations.append("Summarize each main topic")
    
    if len(concepts) > 5:
        recommendations.append("Break content into smaller study sessions")
    
    return recommendations