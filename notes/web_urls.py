from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.notes_list, name='notes_list'),
    path('create/', web_views.create_note, name='create_note'),
    path('upload/', web_views.upload_file, name='upload_file'),
    path('<int:note_id>/', web_views.note_detail, name='note_detail'),
    path('<int:note_id>/summarize/', web_views.summarize_note_view, name='summarize_note'),
]