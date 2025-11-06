from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Note, ContentAnalysis
from .tasks import process_note_async
from .utils.ai_analysis import analyze_content_with_groq, generate_study_recommendations
from .utils.multi_language import translate_and_summarize, get_supported_languages
from .serializers_api import (
    AnalyzeRequestSerializer, AnalyzeResponseSerializer,
    BackgroundTaskSerializer, TaskStatusSerializer,
    TranslateRequestSerializer, TranslateResponseSerializer,
    LanguagesResponseSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    request=AnalyzeRequestSerializer,
    responses={200: AnalyzeResponseSerializer},
    description='Analyze note content with AI and get study recommendations',
    tags=['AI Analysis']
)
@api_view(['POST'])
def analyze_note_content(request, note_id):
    """Analyze note content and provide study recommendations"""
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        
        if not note.original_text:
            return Response(
                {'error': 'No content to analyze'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Analyze content
        analysis = analyze_content_with_groq(note.original_text)
        recommendations = generate_study_recommendations(analysis)
        
        # Store analysis results
        content_analysis, created = ContentAnalysis.objects.get_or_create(
            note=note,
            defaults={
                'key_concepts': analysis.get('key_concepts', []),
                'main_topics': analysis.get('main_topics', []),
                'difficulty_level': analysis.get('difficulty_level', 'intermediate'),
                'estimated_read_time': analysis.get('estimated_read_time', '5 minutes'),
                'subject_area': analysis.get('subject_area', 'General'),
                'study_recommendations': recommendations
            }
        )
        
        if not created:
            # Update existing analysis
            content_analysis.key_concepts = analysis.get('key_concepts', [])
            content_analysis.main_topics = analysis.get('main_topics', [])
            content_analysis.difficulty_level = analysis.get('difficulty_level', 'intermediate')
            content_analysis.estimated_read_time = analysis.get('estimated_read_time', '5 minutes')
            content_analysis.subject_area = analysis.get('subject_area', 'General')
            content_analysis.study_recommendations = recommendations
            content_analysis.save()
        
        return Response({
            'analysis': analysis,
            'recommendations': recommendations,
            'stored': True
        })
        
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=BackgroundTaskSerializer,
    responses={202: TaskStatusSerializer},
    description='Process note asynchronously in background',
    tags=['Background Tasks']
)
@api_view(['POST'])
def process_note_background(request, note_id):
    """Process note summarization and analysis in background"""
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        method = request.data.get('method', 'groq')
        
        # Start background task
        task = process_note_async.delay(note_id, method)
        
        return Response({
            'task_id': task.id,
            'status': 'processing',
            'message': 'Note processing started in background'
        }, status=status.HTTP_202_ACCEPTED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to start background processing: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    responses={200: {'status': str, 'result': dict}},
    description='Check background task status',
    tags=['Background Tasks']
)
@api_view(['GET'])
def check_task_status(request, task_id):
    """Check the status of a background task"""
    try:
        from celery.result import AsyncResult
        
        task = AsyncResult(task_id)
        
        if task.ready():
            return Response({
                'status': 'completed',
                'result': task.result,
                'successful': task.successful()
            })
        else:
            return Response({
                'status': 'processing',
                'result': None,
                'successful': False
            })
            
    except Exception as e:
        return Response(
            {'error': f'Failed to check task status: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    responses={200: {'recommendations': list, 'analysis': dict}},
    description='Get personalized study recommendations',
    tags=['AI Analysis']
)
@api_view(['GET'])
def get_study_recommendations(request, note_id):
    """Get personalized study recommendations for a note"""
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        
        try:
            analysis = note.analysis
            return Response({
                'recommendations': analysis.study_recommendations,
                'analysis': {
                    'key_concepts': analysis.key_concepts,
                    'main_topics': analysis.main_topics,
                    'difficulty_level': analysis.difficulty_level,
                    'estimated_read_time': analysis.estimated_read_time,
                    'subject_area': analysis.subject_area
                }
            })
        except ContentAnalysis.DoesNotExist:
            return Response(
                {'error': 'No analysis available. Please analyze the note first.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        return Response(
            {'error': f'Failed to get recommendations: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=TranslateRequestSerializer,
    responses={200: TranslateResponseSerializer},
    description='Translate note content to target language',
    tags=['Multi-language']
)
@api_view(['POST'])
def translate_note(request, note_id):
    """Translate note content to target language"""
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        target_language = request.data.get('language', 'es')
        method = request.data.get('method', 'groq')
        
        if not note.original_text:
            return Response(
                {'error': 'No content to translate'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = translate_and_summarize(note.original_text, target_language, method)
        
        return Response({
            'translation': result['translation'],
            'summary': result['summary'],
            'target_language': target_language
        })
        
    except Exception as e:
        return Response(
            {'error': f'Translation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    responses={200: LanguagesResponseSerializer},
    description='Get supported languages for translation',
    tags=['Multi-language']
)
@api_view(['GET'])
def get_languages(request):
    """Get list of supported languages"""
    return Response({
        'languages': get_supported_languages()
    })