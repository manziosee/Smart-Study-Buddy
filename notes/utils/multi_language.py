from groq import Groq
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def translate_and_summarize(text, target_language='es', method='groq'):
    """Translate text and create summary in target language"""
    if method == 'groq' and settings.GROQ_API_KEY:
        try:
            client = Groq(api_key=settings.GROQ_API_KEY)
            
            prompt = f"""
            Translate the following text to {target_language} and then provide a concise summary:
            
            Text: {text[:3000]}
            
            Please respond in this format:
            TRANSLATION: [translated text]
            SUMMARY: [summary in {target_language}]
            """
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            
            # Parse response
            if "TRANSLATION:" in result and "SUMMARY:" in result:
                parts = result.split("SUMMARY:")
                translation = parts[0].replace("TRANSLATION:", "").strip()
                summary = parts[1].strip()
                return {"translation": translation, "summary": summary}
            
            return {"translation": result, "summary": result[:500]}
            
        except Exception as e:
            logger.error(f"Groq translation failed: {e}")
    
    return {"translation": text, "summary": text[:500]}

def get_supported_languages():
    """Return list of supported languages"""
    return {
        'es': 'Spanish',
        'fr': 'French', 
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi'
    }