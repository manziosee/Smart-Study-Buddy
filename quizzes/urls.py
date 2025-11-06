from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/generate/', views.generate_quiz, name='generate-quiz'),
    path('quiz/submit/', views.submit_quiz, name='submit-quiz'),
    path('quiz/attempts/', views.QuizAttemptListView.as_view(), name='quiz-attempts'),
]