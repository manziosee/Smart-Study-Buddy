from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .utils import update_study_analytics, generate_study_recommendations, get_learning_insights

@extend_schema(
    responses={200: {'analytics': dict, 'insights': dict}},
    description='Get comprehensive study analytics and insights',
    tags=['Analytics']
)
@api_view(['GET'])
def get_study_analytics(request):
    """Get user's study analytics and insights"""
    try:
        analytics = update_study_analytics(request.user)
        insights = get_learning_insights(request.user)
        recommendations = generate_study_recommendations(request.user)
        
        return Response({
            'analytics': {
                'total_notes': analytics.notes_created,
                'total_quizzes': analytics.quizzes_taken,
                'average_score': analytics.average_quiz_score,
                'study_streak': analytics.study_streak,
                'last_study_date': analytics.last_study_date
            },
            'insights': insights,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to get analytics: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@extend_schema(
    responses={200: {'dashboard': dict}},
    description='Get dashboard data with key metrics',
    tags=['Analytics']
)
@api_view(['GET'])
def get_dashboard_data(request):
    """Get dashboard summary data"""
    try:
        analytics = update_study_analytics(request.user)
        
        return Response({
            'dashboard': {
                'notes_count': analytics.notes_created,
                'quizzes_taken': analytics.quizzes_taken,
                'average_score': analytics.average_quiz_score,
                'study_streak': analytics.study_streak,
                'performance_grade': 'A' if analytics.average_quiz_score >= 90 else 
                                   'B' if analytics.average_quiz_score >= 80 else
                                   'C' if analytics.average_quiz_score >= 70 else 'D'
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Failed to get dashboard data: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )