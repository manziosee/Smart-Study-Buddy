# from transformers import pipeline
import os
from django.conf import settings
import requests


def summarize_with_huggingface(text, max_length=200, min_length=50):
    """Simple text summarization fallback"""
    try:
        # Simple extractive summarization - take first few sentences
        sentences = text.split('. ')
        if len(sentences) <= 3:
            return text
        
        # Take first 3 sentences as summary
        summary = '. '.join(sentences[:3]) + '.'
        return summary if len(summary) > 50 else text[:200] + "..."
    
    except Exception as e:
        return text[:200] + "..."


def summarize_with_groq(text):
    """Summarize text using Groq API"""
    api_key = settings.GROQ_API_KEY
    if not api_key or api_key == 'your_groq_key_here':
        return summarize_with_huggingface(text)
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are an expert at creating concise, informative summaries. Summarize the following text in 2-3 paragraphs, focusing on key concepts and main ideas.'
                },
                {
                    'role': 'user',
                    'content': f'Please summarize this text: {text}'
                }
            ],
            'model': 'llama3-8b-8192',
            'temperature': 0.3,
            'max_tokens': 500
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            # Try Hugging Face API as fallback
            from .huggingface_api import summarize_with_hf_api
            return summarize_with_hf_api(text)
            
    except Exception as e:
        # Try Hugging Face API as fallback
        from .huggingface_api import summarize_with_hf_api
        return summarize_with_hf_api(text)


def summarize_text(text, method='huggingface'):
    """Main summarization function"""
    if not text or len(text.strip()) < 100:
        return "Text too short to summarize."
    
    if method == 'groq':
        return summarize_with_groq(text)
    else:
        return summarize_with_huggingface(text)