from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'correct_answer', 'explanation', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'created_at', 'questions']


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'total_questions', 'completed_at']
        read_only_fields = ['id', 'completed_at']


class GenerateQuizSerializer(serializers.Serializer):
    note_id = serializers.IntegerField()
    num_questions = serializers.IntegerField(default=5, min_value=1, max_value=20)
    method = serializers.ChoiceField(choices=['huggingface', 'simple'], default='huggingface')


class SubmitQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(child=serializers.CharField())


class QuizResultSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    score = serializers.IntegerField()
    total_questions = serializers.IntegerField()
    percentage = serializers.FloatField()
    results = serializers.ListField()