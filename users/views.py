from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer
from .serializers_api import LogoutResponseSerializer


@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: UserSerializer, 400: OpenApiResponse(description='Validation errors')},
    description='Register a new user account',
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={200: UserSerializer, 401: OpenApiResponse(description='Invalid credentials')},
    description='Login with email and password',
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email and password:
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: LogoutResponseSerializer},
    description='Logout current user',
    tags=['Authentication']
)
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})


@extend_schema(
    responses={200: UserSerializer},
    description='Get or update user profile',
    tags=['Authentication']
)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user