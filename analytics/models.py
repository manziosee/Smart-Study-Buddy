from django.db import models
from django.contrib.auth import get_user_model
from notes.models import Note
from quizzes.models import Quiz, QuizAttempt

User = get_user_model()

class StudyAnalytics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    total_study_time = models.DurationField(default='00:00:00')
    notes_created = models.IntegerField(default=0)
    quizzes_taken = models.IntegerField(default=0)
    average_quiz_score = models.FloatField(default=0.0)
    study_streak = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LearningPattern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_patterns')
    subject_area = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ])
    time_spent = models.DurationField(default='00:00:00')
    success_rate = models.FloatField(default=0.0)
    last_activity = models.DateTimeField(auto_now=True)

class StudyRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommendation_type = models.CharField(max_length=50, choices=[
        ('review', 'Review Material'),
        ('practice', 'Practice Quiz'),
        ('study', 'Study New Topic'),
        ('break', 'Take a Break')
    ])
    priority = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)