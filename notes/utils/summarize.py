from transformers import pipeline
import os
from django.conf import settings
import requests


def summarize_with_huggingface(text, max_length=200, min_length=50):
    """Summarize text using Hugging Face transformers"""
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Split text into chunks if too long
        max_chunk_length = 1024
        if len(text) > max_chunk_length:
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            summaries = []
            
            for chunk in chunks:
                if len(chunk.strip()) > 100:  # Only summarize meaningful chunks
                    summary = summarizer(chunk, max_length=max_length//len(chunks), 
                                       min_length=min_length//len(chunks), do_sample=False)
                    summaries.append(summary[0]['summary_text'])
            
            return ' '.join(summaries)
        else:
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
    
    except Exception as e:
        raise Exception(f"Summarization failed: {str(e)}")


def summarize_with_groq(text):
    """Summarize text using Groq API (placeholder implementation)"""
    # This is a placeholder - implement actual Groq API integration
    api_key = settings.GROQ_API_KEY
    if not api_key or api_key == 'your_groq_key_here':
        # Fallback to Hugging Face
        return summarize_with_huggingface(text)
    
    # TODO: Implement actual Groq API call
    # For now, fallback to Hugging Face
    return summarize_with_huggingface(text)


def summarize_text(text, method='huggingface'):
    """Main summarization function"""
    if not text or len(text.strip()) < 100:
        return "Text too short to summarize."
    
    if method == 'groq':
        return summarize_with_groq(text)
    else:
        return summarize_with_huggingface(text)