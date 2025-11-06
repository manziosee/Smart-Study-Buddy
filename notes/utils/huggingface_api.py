import requests
import os
from django.conf import settings

def summarize_with_hf_api(text, max_length=200):
    """Summarize text using Hugging Face Inference API"""
    api_token = settings.HUGGINGFACE_API_TOKEN
    if not api_token or api_token == 'your_token_here':
        return text[:200] + "..."
    
    try:
        headers = {"Authorization": f"Bearer {api_token}"}
        
        # Use BART model for summarization
        api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        
        payload = {
            "inputs": text[:1024],  # Limit input length
            "parameters": {
                "max_length": max_length,
                "min_length": 50,
                "do_sample": False
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('summary_text', text[:200] + "...")
            return text[:200] + "..."
        else:
            return text[:200] + "..."
            
    except Exception as e:
        return text[:200] + "..."

def generate_questions_with_hf_api(text, num_questions=3):
    """Generate questions using Hugging Face API"""
    api_token = settings.HUGGINGFACE_API_TOKEN
    if not api_token or api_token == 'your_token_here':
        return []
    
    try:
        headers = {"Authorization": f"Bearer {api_token}"}
        
        # Use T5 model for question generation
        api_url = "https://api-inference.huggingface.co/models/valhalla/t5-small-qg-hl"
        
        sentences = text.split('. ')[:num_questions]
        questions = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 20:
                payload = {
                    "inputs": f"generate question: {sentence}",
                    "parameters": {"max_length": 64}
                }
                
                response = requests.post(api_url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        question_text = result[0].get('generated_text', f'Question {i+1}?')
                        
                        questions.append({
                            'question': question_text,
                            'type': 'mcq',
                            'choices': [
                                {'text': 'Option A', 'is_correct': True},
                                {'text': 'Option B', 'is_correct': False},
                                {'text': 'Option C', 'is_correct': False},
                                {'text': 'Option D', 'is_correct': False}
                            ],
                            'correct_answer': 'Option A',
                            'explanation': f'Based on: {sentence[:100]}...'
                        })
        
        return questions
        
    except Exception as e:
        return []