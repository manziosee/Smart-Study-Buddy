from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User
from .serializers_api import UserRegistrationSerializer, UserProfileSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login user and return JWT tokens"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        
        # Check if account is locked
        if user.is_account_locked:
            return Response({
                'error': 'Account is temporarily locked due to failed login attempts'
            }, status=status.HTTP_423_LOCKED)
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user:
            # Reset failed attempts on successful login
            user.failed_login_attempts = 0
            user.last_login_ip = request.META.get('REMOTE_ADDR')
            user.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            # Increment failed attempts
            user = User.objects.get(email=email)
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.lock_account(30)  # Lock for 30 minutes
                
            user.save()
            
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logout_view(request):
    """Logout user by blacklisting refresh token"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Successfully logged out'})
    except Exception:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile_view(request):
    """Get user profile"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_profile_view(request):
    """Update user profile"""
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)