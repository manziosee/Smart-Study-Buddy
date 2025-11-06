from rest_framework import serializers

class AnalyzeRequestSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['groq', 'huggingface'], default='groq')

class AnalyzeResponseSerializer(serializers.Serializer):
    analysis = serializers.DictField()
    recommendations = serializers.ListField()
    stored = serializers.BooleanField()

class BackgroundTaskSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['groq', 'huggingface'], default='groq')

class TaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()

class TranslateRequestSerializer(serializers.Serializer):
    language = serializers.CharField(max_length=10)
    method = serializers.ChoiceField(choices=['groq'], default='groq')

class TranslateResponseSerializer(serializers.Serializer):
    translation = serializers.CharField()
    summary = serializers.CharField()
    target_language = serializers.CharField()

class LanguagesResponseSerializer(serializers.Serializer):
    languages = serializers.DictField()