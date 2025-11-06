from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz


@login_required
def quizzes_list(request):
    """List all user quizzes"""
    quizzes = Quiz.objects.filter(note__user=request.user)
    return render(request, 'quizzes/list.html', {'quizzes': quizzes})


@login_required
def quiz_detail(request, quiz_id):
    """View quiz details"""
    quiz = get_object_or_404(Quiz, id=quiz_id, note__user=request.user)
    return render(request, 'quizzes/detail.html', {'quiz': quiz})