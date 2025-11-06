from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('upload/', views.NoteUploadView.as_view(), name='note-upload'),
    path('notes/<int:note_id>/summarize/', views.summarize_note, name='summarize-note'),
    path('summarize/', views.summarize_text_view, name='summarize-text'),
]