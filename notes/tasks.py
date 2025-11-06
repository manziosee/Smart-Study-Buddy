from celery import shared_task
from django.core.mail import send_mail
from .models import Note
from .utils.summarize import summarize_text
from .utils.ai_analysis import analyze_content_with_groq, generate_study_recommendations
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_note_async(note_id, method='groq'):
    """Process note summarization and analysis in background"""
    try:
        note = Note.objects.get(id=note_id)
        
        # Generate summary
        if not note.summary and note.original_text:
            summary = summarize_text(note.original_text, method=method)
            note.summary = summary
            note.save()
        
        # Analyze content
        analysis = analyze_content_with_groq(note.original_text)
        
        # Generate recommendations
        recommendations = generate_study_recommendations(analysis)
        
        # Store analysis results (you might want to create a model for this)
        logger.info(f"Processed note {note_id}: {len(recommendations)} recommendations generated")
        
        return {
            'note_id': note_id,
            'summary_generated': bool(note.summary),
            'analysis': analysis,
            'recommendations': recommendations
        }
        
    except Note.DoesNotExist:
        logger.error(f"Note {note_id} not found")
        return {'error': 'Note not found'}
    except Exception as e:
        logger.error(f"Error processing note {note_id}: {str(e)}")
        return {'error': str(e)}


@shared_task
def batch_process_notes(user_id):
    """Process multiple notes for a user"""
    try:
        notes = Note.objects.filter(user_id=user_id, summary__isnull=True)
        results = []
        
        for note in notes[:5]:  # Limit to 5 notes at a time
            result = process_note_async.delay(note.id)
            results.append(result.id)
        
        return {'processed_tasks': results}
        
    except Exception as e:
        logger.error(f"Error batch processing notes for user {user_id}: {str(e)}")
        return {'error': str(e)}


@shared_task
def send_study_reminder(user_id, note_id):
    """Send study reminder email"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        note = Note.objects.get(id=note_id)
        
        send_mail(
            subject='Study Reminder - Smart Study Buddy',
            message=f'Hi {user.username},\n\nDon\'t forget to review your note: "{note.title}"\n\nHappy studying!',
            from_email='noreply@smartstudybuddy.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return {'status': 'sent', 'user': user.username, 'note': note.title}
        
    except Exception as e:
        logger.error(f"Error sending reminder: {str(e)}")
        return {'error': str(e)}