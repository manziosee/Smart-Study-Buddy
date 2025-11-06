import django_filters
from django.db import models
from .models import Quiz, QuizAttempt


class QuizFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    note_title = django_filters.CharFilter(field_name='note__title', lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    min_questions = django_filters.NumberFilter(method='filter_min_questions')
    
    class Meta:
        model = Quiz
        fields = ['title', 'note_title', 'created_after', 'created_before', 'min_questions']
    
    def filter_min_questions(self, queryset, name, value):
        return queryset.annotate(
            question_count=models.Count('questions')
        ).filter(question_count__gte=value)


class QuizAttemptFilter(django_filters.FilterSet):
    quiz_title = django_filters.CharFilter(field_name='quiz__title', lookup_expr='icontains')
    min_score = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    max_score = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    min_percentage = django_filters.NumberFilter(method='filter_min_percentage')
    attempted_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    attempted_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = QuizAttempt
        fields = ['quiz_title', 'min_score', 'max_score', 'min_percentage', 'attempted_after', 'attempted_before']
    
    def filter_min_percentage(self, queryset, name, value):
        return queryset.annotate(
            percentage=models.Case(
                models.When(total_questions=0, then=0),
                default=models.F('score') * 100.0 / models.F('total_questions'),
                output_field=models.FloatField()
            )
        ).filter(percentage__gte=value)