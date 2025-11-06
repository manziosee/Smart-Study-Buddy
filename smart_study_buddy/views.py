from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from notes.models import Note
from quizzes.models import Quiz, QuizAttempt
from users.serializers import UserRegistrationSerializer


def home(request):
    """Home page - show landing page or redirect to dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


@login_required
def dashboard(request):
    """Main dashboard view"""
    # Get user statistics
    stats = {
        'notes_count': Note.objects.filter(user=request.user).count(),
        'summaries_count': Note.objects.filter(user=request.user, summary__isnull=False).exclude(summary='').count(),
        'quizzes_count': Quiz.objects.filter(note__user=request.user).count(),
        'quiz_attempts': QuizAttempt.objects.filter(user=request.user).count(),
    }
    
    # Get recent activity
    recent_notes = Note.objects.filter(user=request.user)[:5]
    recent_quizzes = Quiz.objects.filter(note__user=request.user)[:5]
    
    context = {
        'stats': stats,
        'recent_notes': recent_notes,
        'recent_quizzes': recent_quizzes,
    }
    return render(request, 'dashboard.html', context)


def login_view(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth/login.html')


def register_view(request):
    """Registration view"""
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return render(request, 'auth/register.html')


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'auth/profile.html')