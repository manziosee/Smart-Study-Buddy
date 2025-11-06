# from transformers import pipeline
import re
import random


def generate_questions_huggingface(text, num_questions=5):
    """Simple question generation without transformers"""
    return generate_simple_questions(text, num_questions)


def generate_mcq_choices(context, question):
    """Generate multiple choice options"""
    # Extract key terms from context
    words = re.findall(r'\b[A-Z][a-z]+\b|\b\d+\b', context)
    
    if not words:
        return [
            {'text': 'Option A', 'is_correct': True},
            {'text': 'Option B', 'is_correct': False},
            {'text': 'Option C', 'is_correct': False},
            {'text': 'Option D', 'is_correct': False},
        ]
    
    # Use first word as correct answer, generate distractors
    correct = words[0] if words else "Correct Answer"
    distractors = words[1:4] if len(words) > 3 else ["Option B", "Option C", "Option D"]
    
    choices = [{'text': correct, 'is_correct': True}]
    for distractor in distractors[:3]:
        choices.append({'text': distractor, 'is_correct': False})
    
    # Shuffle choices
    random.shuffle(choices)
    return choices


def generate_simple_questions(text, num_questions=5):
    """Fallback simple question generation"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    questions = []
    
    for i in range(min(num_questions, len(sentences))):
        sentence = sentences[i]
        
        # Simple question templates
        templates = [
            f"What is mentioned about {extract_subject(sentence)}?",
            f"According to the text, what happens when {extract_action(sentence)}?",
            f"Which of the following is true about {extract_subject(sentence)}?",
        ]
        
        question_text = random.choice(templates)
        choices = generate_mcq_choices(sentence, question_text)
        
        questions.append({
            'question': question_text,
            'type': 'mcq',
            'choices': choices,
            'correct_answer': choices[0]['text'],
            'explanation': f"Based on: {sentence[:100]}..."
        })
    
    return questions


def extract_subject(sentence):
    """Extract main subject from sentence"""
    words = sentence.split()
    # Simple heuristic: find first noun-like word
    for word in words:
        if len(word) > 3 and word[0].isupper():
            return word
    return "the topic"


def extract_action(sentence):
    """Extract main action from sentence"""
    # Simple heuristic: find verb-like words
    common_verbs = ['is', 'are', 'was', 'were', 'has', 'have', 'will', 'can', 'does']
    words = sentence.split()
    
    for word in words:
        if word.lower() in common_verbs:
            return word.lower()
    return "something occurs"


def generate_quiz_from_text(text, num_questions=5, method='huggingface'):
    """Main function to generate quiz from text"""
    if not text or len(text.strip()) < 100:
        return []
    
    if method == 'huggingface':
        from ..notes.utils.huggingface_api import generate_questions_with_hf_api
        hf_questions = generate_questions_with_hf_api(text, num_questions)
        return hf_questions if hf_questions else generate_simple_questions(text, num_questions)
    else:
        return generate_simple_questions(text, num_questions)