from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'original_text']
    readonly_fields = ['created_at', 'updated_at']