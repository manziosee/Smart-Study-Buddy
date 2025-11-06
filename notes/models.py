from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    original_text = models.TextField()
    summary = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContentAnalysis(models.Model):
    """Store AI analysis results for notes"""
    note = models.OneToOneField(Note, on_delete=models.CASCADE, related_name='analysis')
    key_concepts = models.JSONField(default=list)
    main_topics = models.JSONField(default=list)
    difficulty_level = models.CharField(max_length=20, default='intermediate')
    estimated_read_time = models.CharField(max_length=50, default='5 minutes')
    subject_area = models.CharField(max_length=100, default='General')
    study_recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.note.title}"


class StudySession(models.Model):
    """Track user study sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='study_sessions')
    duration_minutes = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.note.title} ({self.duration_minutes}min)"