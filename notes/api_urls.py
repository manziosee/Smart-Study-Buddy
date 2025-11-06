from django.urls import path
from . import api_views


urlpatterns = [
    path('notes/<int:note_id>/analyze/', api_views.analyze_note_content, name='analyze-note'),
    path('notes/<int:note_id>/process-background/', api_views.process_note_background, name='process-background'),
    path('tasks/<str:task_id>/status/', api_views.check_task_status, name='task-status'),
    path('notes/<int:note_id>/recommendations/', api_views.get_study_recommendations, name='study-recommendations'),
    path('notes/<int:note_id>/translate/', api_views.translate_note, name='translate-note'),
    path('languages/', api_views.get_languages, name='supported-languages'),
]