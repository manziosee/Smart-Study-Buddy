import django_filters
from django.db import models
from .models import Note


class NoteFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    has_summary = django_filters.BooleanFilter(method='filter_has_summary')
    has_file = django_filters.BooleanFilter(method='filter_has_file')
    
    class Meta:
        model = Note
        fields = ['title', 'created_after', 'created_before', 'has_summary', 'has_file']
    
    def filter_has_summary(self, queryset, name, value):
        if value:
            return queryset.exclude(summary__isnull=True).exclude(summary__exact='')
        return queryset.filter(models.Q(summary__isnull=True) | models.Q(summary__exact=''))
    
    def filter_has_file(self, queryset, name, value):
        if value:
            return queryset.exclude(file__isnull=True).exclude(file__exact='')
        return queryset.filter(models.Q(file__isnull=True) | models.Q(file__exact=''))