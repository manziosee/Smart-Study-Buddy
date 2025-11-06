import requests
from django.conf import settings
import json
import random
import re


def generate_advanced_quiz_with_groq(text, num_questions=5, question_types=['mcq', 'tf', 'fill']):
    """Generate advanced quiz questions using Groq API"""
    api_key = settings.GROQ_API_KEY
    if not api_key or api_key == 'your_groq_key_here':
        return generate_fallback_quiz(text, num_questions)
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Create different question types
        all_questions = []
        
        for q_type in question_types:
            questions = generate_questions_by_type(text, q_type, num_questions // len(question_types), headers)
            all_questions.extend(questions)
        
        # Fill remaining questions with MCQ if needed
        while len(all_questions) < num_questions:
            mcq_questions = generate_questions_by_type(text, 'mcq', 1, headers)
            all_questions.extend(mcq_questions)
        
        return all_questions[:num_questions]
        
    except Exception as e:
        return generate_fallback_quiz(text, num_questions)


def generate_questions_by_type(text, question_type, count, headers):
    """Generate specific type of questions"""
    if question_type == 'mcq':
        return generate_mcq_questions(text, count, headers)
    elif question_type == 'tf':
        return generate_true_false_questions(text, count, headers)
    elif question_type == 'fill':
        return generate_fill_blank_questions(text, count, headers)
    else:
        return generate_mcq_questions(text, count, headers)


def generate_mcq_questions(text, count, headers):
    """Generate multiple choice questions"""
    payload = {
        'messages': [
            {
                'role': 'system',
                'content': f'''Create {count} multiple choice questions from the text. Return JSON format:
                {{
                    "questions": [
                        {{
                            "question": "Question text?",
                            "choices": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                            "correct_answer": "A) Option 1",
                            "explanation": "Why this is correct"
                        }}
                    ]
                }}'''
            },
            {
                'role': 'user',
                'content': f'Text: {text[:1500]}'
            }
        ],
        'model': 'llama3-8b-8192',
        'temperature': 0.4,
        'max_tokens': 800
    }
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            try:
                data = json.loads(content)
                questions = []
                for q in data.get('questions', []):
                    choices = []
                    for choice in q.get('choices', []):
                        choices.append({
                            'text': choice,
                            'is_correct': choice == q.get('correct_answer')
                        })
                    
                    questions.append({
                        'question': q.get('question'),
                        'type': 'mcq',
                        'choices': choices,
                        'correct_answer': q.get('correct_answer'),
                        'explanation': q.get('explanation', '')
                    })
                return questions
            except json.JSONDecodeError:
                return parse_mcq_from_text(content)
        
    except Exception:
        pass
    
    return []


def generate_true_false_questions(text, count, headers):
    """Generate true/false questions"""
    payload = {
        'messages': [
            {
                'role': 'system',
                'content': f'''Create {count} true/false questions from the text. Return JSON format:
                {{
                    "questions": [
                        {{
                            "statement": "Statement to evaluate",
                            "correct_answer": true,
                            "explanation": "Why this is true/false"
                        }}
                    ]
                }}'''
            },
            {
                'role': 'user',
                'content': f'Text: {text[:1500]}'
            }
        ],
        'model': 'llama3-8b-8192',
        'temperature': 0.3,
        'max_tokens': 600
    }
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            try:
                data = json.loads(content)
                questions = []
                for q in data.get('questions', []):
                    choices = [
                        {'text': 'True', 'is_correct': q.get('correct_answer', True)},
                        {'text': 'False', 'is_correct': not q.get('correct_answer', True)}
                    ]
                    
                    questions.append({
                        'question': q.get('statement'),
                        'type': 'tf',
                        'choices': choices,
                        'correct_answer': 'True' if q.get('correct_answer') else 'False',
                        'explanation': q.get('explanation', '')
                    })
                return questions
            except json.JSONDecodeError:
                return []
        
    except Exception:
        pass
    
    return []


def generate_fill_blank_questions(text, count, headers):
    """Generate fill-in-the-blank questions"""
    payload = {
        'messages': [
            {
                'role': 'system',
                'content': f'''Create {count} fill-in-the-blank questions from the text. Return JSON format:
                {{
                    "questions": [
                        {{
                            "question": "The _____ is responsible for _____.",
                            "correct_answer": "brain, thinking",
                            "explanation": "Explanation of the answer"
                        }}
                    ]
                }}'''
            },
            {
                'role': 'user',
                'content': f'Text: {text[:1500]}'
            }
        ],
        'model': 'llama3-8b-8192',
        'temperature': 0.3,
        'max_tokens': 600
    }
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            try:
                data = json.loads(content)
                questions = []
                for q in data.get('questions', []):
                    questions.append({
                        'question': q.get('question'),
                        'type': 'fill',
                        'choices': [],
                        'correct_answer': q.get('correct_answer'),
                        'explanation': q.get('explanation', '')
                    })
                return questions
            except json.JSONDecodeError:
                return []
        
    except Exception:
        pass
    
    return []


def parse_mcq_from_text(text):
    """Parse MCQ questions from text response"""
    questions = []
    # Basic parsing logic for when JSON parsing fails
    question_blocks = re.split(r'\n\s*\n', text)
    
    for block in question_blocks:
        if '?' in block and 'A)' in block:
            lines = block.strip().split('\n')
            question = lines[0].strip()
            choices = []
            correct = None
            
            for line in lines[1:]:
                if re.match(r'^[A-D]\)', line):
                    choices.append({'text': line.strip(), 'is_correct': False})
                elif 'correct' in line.lower():
                    correct = line.strip()
            
            if choices and len(choices) >= 2:
                if correct:
                    for choice in choices:
                        if correct.split()[-1] in choice['text']:
                            choice['is_correct'] = True
                else:
                    choices[0]['is_correct'] = True
                
                questions.append({
                    'question': question,
                    'type': 'mcq',
                    'choices': choices,
                    'correct_answer': next((c['text'] for c in choices if c['is_correct']), choices[0]['text']),
                    'explanation': 'Generated from content analysis'
                })
    
    return questions


def generate_fallback_quiz(text, num_questions):
    """Fallback quiz generation without AI"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    questions = []
    for i in range(min(num_questions, len(sentences))):
        sentence = sentences[i]
        words = sentence.split()
        
        if len(words) > 5:
            # Create a simple fill-in-the-blank
            blank_word = random.choice(words[2:-2])
            question_text = sentence.replace(blank_word, '_____')
            
            questions.append({
                'question': question_text,
                'type': 'fill',
                'choices': [],
                'correct_answer': blank_word,
                'explanation': f'Based on: {sentence}'
            })
    
    return questions