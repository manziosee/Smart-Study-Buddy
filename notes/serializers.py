from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'original_text', 'summary', 'file', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NoteUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'file']


class SummarizeSerializer(serializers.Serializer):
    text = serializers.CharField()
    method = serializers.ChoiceField(choices=['huggingface', 'groq'], default='huggingface')


class SummaryResponseSerializer(serializers.Serializer):
    summary = serializers.CharField()


class SummarizeNoteSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['huggingface', 'groq'], default='huggingface')