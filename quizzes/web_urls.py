from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.quizzes_list, name='quizzes_list'),
    path('<int:quiz_id>/', web_views.quiz_detail, name='quiz_detail'),
]