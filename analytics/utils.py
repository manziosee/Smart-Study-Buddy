from django.utils import timezone
from django.db.models import Avg, Count, Sum
from datetime import timedelta
from .models import StudyAnalytics, LearningPattern, StudyRecommendation
from quizzes.models import QuizAttempt
from notes.models import Note

def update_study_analytics(user):
    """Update user's study analytics"""
    analytics, created = StudyAnalytics.objects.get_or_create(user=user)
    
    # Update basic stats
    analytics.notes_created = Note.objects.filter(user=user).count()
    analytics.quizzes_taken = QuizAttempt.objects.filter(user=user).count()
    
    # Calculate average quiz score
    avg_score = QuizAttempt.objects.filter(user=user).aggregate(
        avg=Avg('score')
    )['avg'] or 0.0
    analytics.average_quiz_score = round(avg_score, 2)
    
    # Update study streak
    today = timezone.now().date()
    if analytics.last_study_date:
        days_diff = (today - analytics.last_study_date).days
        if days_diff == 1:
            analytics.study_streak += 1
        elif days_diff > 1:
            analytics.study_streak = 1
    else:
        analytics.study_streak = 1
    
    analytics.last_study_date = today
    analytics.save()
    
    return analytics

def generate_study_recommendations(user):
    """Generate personalized study recommendations"""
    analytics = user.analytics if hasattr(user, 'analytics') else None
    recommendations = []
    
    if not analytics:
        recommendations.append({
            'title': 'Welcome! Create your first note',
            'description': 'Start by uploading a document or creating a note to begin your learning journey.',
            'type': 'study',
            'priority': 1
        })
        return recommendations
    
    # Low quiz performance recommendation
    if analytics.average_quiz_score < 70:
        recommendations.append({
            'title': 'Review your study materials',
            'description': 'Your quiz scores suggest reviewing notes before taking more quizzes.',
            'type': 'review',
            'priority': 2
        })
    
    # Study streak encouragement
    if analytics.study_streak >= 7:
        recommendations.append({
            'title': 'Amazing streak! Keep it up!',
            'description': f'You\'ve studied for {analytics.study_streak} days straight. Consider a short break.',
            'type': 'break',
            'priority': 3
        })
    
    # New content suggestion
    recent_notes = Note.objects.filter(
        user=user,
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    if recent_notes == 0:
        recommendations.append({
            'title': 'Add new study material',
            'description': 'You haven\'t added new notes recently. Try uploading a new document.',
            'type': 'study',
            'priority': 1
        })
    
    return recommendations

def get_learning_insights(user):
    """Get detailed learning insights for user"""
    analytics = user.analytics if hasattr(user, 'analytics') else None
    if not analytics:
        return {}
    
    # Recent performance
    recent_attempts = QuizAttempt.objects.filter(
        user=user,
        created_at__gte=timezone.now() - timedelta(days=30)
    )
    
    performance_trend = []
    for attempt in recent_attempts.order_by('created_at')[:10]:
        percentage = (attempt.score / attempt.total_questions * 100) if attempt.total_questions > 0 else 0
        performance_trend.append({
            'date': attempt.created_at.strftime('%Y-%m-%d'),
            'score': percentage,
            'quiz': attempt.quiz.title
        })
    
    return {
        'total_notes': analytics.notes_created,
        'total_quizzes': analytics.quizzes_taken,
        'average_score': analytics.average_quiz_score,
        'study_streak': analytics.study_streak,
        'performance_trend': performance_trend,
        'last_study': analytics.last_study_date
    }