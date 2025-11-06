from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.get_study_analytics, name='study-analytics'),
    path('dashboard/', views.get_dashboard_data, name='dashboard-data'),
]