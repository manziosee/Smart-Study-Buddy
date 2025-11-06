from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from notes.models import Note
from .models import Quiz, Question, Choice, QuizAttempt
from .serializers import (
    QuizSerializer, QuizAttemptSerializer, GenerateQuizSerializer, 
    SubmitQuizSerializer, QuizResultSerializer
)
from .utils.quiz_generator import generate_quiz_from_text


@extend_schema(
    responses={200: QuizSerializer(many=True)},
    description='List all quizzes for the authenticated user',
    tags=['Quizzes']
)
class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        return Quiz.objects.filter(note__user=self.request.user)


@extend_schema(
    responses={200: QuizSerializer, 404: OpenApiResponse(description='Quiz not found')},
    description='Retrieve a specific quiz with questions',
    tags=['Quizzes']
)
class QuizDetailView(generics.RetrieveAPIView):
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        return Quiz.objects.filter(note__user=self.request.user)


@extend_schema(
    request=GenerateQuizSerializer,
    responses={201: QuizSerializer, 400: OpenApiResponse(description='Quiz generation failed')},
    description='Generate a quiz from a note using AI',
    tags=['Quizzes']
)
@api_view(['POST'])
def generate_quiz(request):
    """Generate a quiz from a note"""
    serializer = GenerateQuizSerializer(data=request.data)
    if serializer.is_valid():
        note_id = serializer.validated_data['note_id']
        num_questions = serializer.validated_data['num_questions']
        method = serializer.validated_data['method']
        
        try:
            note = get_object_or_404(Note, id=note_id, user=request.user)
            
            if not note.original_text and not note.summary:
                return Response(
                    {'error': 'No text content available for quiz generation'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Use summary if available, otherwise use original text
            text_content = note.summary if note.summary else note.original_text
            
            # Generate questions
            questions_data = generate_quiz_from_text(text_content, num_questions, method)
            
            if not questions_data:
                return Response(
                    {'error': 'Failed to generate questions from the text'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create quiz
            quiz = Quiz.objects.create(
                note=note,
                title=f"Quiz for {note.title}"
            )
            
            # Create questions and choices
            for q_data in questions_data:
                question = Question.objects.create(
                    quiz=quiz,
                    question_text=q_data['question'],
                    question_type=q_data['type'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data.get('explanation', '')
                )
                
                # Create choices for MCQ
                if q_data['type'] == 'mcq' and 'choices' in q_data:
                    for choice_data in q_data['choices']:
                        Choice.objects.create(
                            question=question,
                            choice_text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )
            
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'error': f'Quiz generation failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SubmitQuizSerializer,
    responses={200: QuizResultSerializer, 404: OpenApiResponse(description='Quiz not found')},
    description='Submit quiz answers and get score with detailed results',
    tags=['Quizzes']
)
@api_view(['POST'])
def submit_quiz(request):
    """Submit quiz answers and get score"""
    serializer = SubmitQuizSerializer(data=request.data)
    if serializer.is_valid():
        quiz_id = serializer.validated_data['quiz_id']
        answers = serializer.validated_data['answers']
        
        try:
            quiz = get_object_or_404(Quiz, id=quiz_id, note__user=request.user)
            questions = quiz.questions.all()
            
            score = 0
            total_questions = len(questions)
            results = []
            
            for question in questions:
                question_id = str(question.id)
                user_answer = answers.get(question_id, '')
                
                is_correct = False
                if question.question_type == 'mcq':
                    # For MCQ, check if the selected choice is correct
                    try:
                        selected_choice = question.choices.get(choice_text=user_answer)
                        is_correct = selected_choice.is_correct
                    except Choice.DoesNotExist:
                        is_correct = False
                else:
                    # For other types, simple text comparison
                    is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
                
                if is_correct:
                    score += 1
                
                results.append({
                    'question_id': question.id,
                    'question': question.question_text,
                    'user_answer': user_answer,
                    'correct_answer': question.correct_answer,
                    'is_correct': is_correct,
                    'explanation': question.explanation
                })
            
            # Save quiz attempt
            attempt = QuizAttempt.objects.create(
                quiz=quiz,
                user=request.user,
                score=score,
                total_questions=total_questions
            )
            
            return Response({
                'attempt_id': attempt.id,
                'score': score,
                'total_questions': total_questions,
                'percentage': round((score / total_questions) * 100, 2) if total_questions > 0 else 0,
                'results': results
            })
        
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'error': f'Quiz submission failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: QuizAttemptSerializer(many=True)},
    description='List all quiz attempts for the authenticated user',
    tags=['Quizzes']
)
class QuizAttemptListView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user)