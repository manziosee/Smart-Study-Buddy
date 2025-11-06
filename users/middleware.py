from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class SecurityMiddleware:
    """Middleware for enhanced security features"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Track user IP on login
        if request.user.is_authenticated and hasattr(request.user, 'last_login_ip'):
            current_ip = request.META.get('REMOTE_ADDR')
            if request.user.last_login_ip != current_ip:
                request.user.last_login_ip = current_ip
                request.user.save(update_fields=['last_login_ip'])

        response = self.get_response(request)
        return response