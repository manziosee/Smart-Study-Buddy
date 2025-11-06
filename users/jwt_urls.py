from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import jwt_views

urlpatterns = [
    path('register/', jwt_views.register_view, name='jwt_register'),
    path('login/', jwt_views.login_view, name='jwt_login'),
    path('logout/', jwt_views.logout_view, name='jwt_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('profile/', jwt_views.profile_view, name='jwt_profile'),
    path('profile/update/', jwt_views.update_profile_view, name='jwt_profile_update'),
]