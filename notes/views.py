from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Note
from .serializers import NoteSerializer, NoteUploadSerializer, SummarizeSerializer, SummaryResponseSerializer, SummarizeNoteSerializer
from .utils.extract_text import extract_text_from_file, clean_text
from .utils.summarize import summarize_text


@extend_schema(
    responses={200: NoteSerializer(many=True), 201: NoteSerializer},
    description='List user notes or create a new note',
    tags=['Notes']
)
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    responses={200: NoteSerializer, 404: OpenApiResponse(description='Note not found')},
    description='Retrieve, update or delete a specific note',
    tags=['Notes']
)
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


@extend_schema(
    request=NoteUploadSerializer,
    responses={201: NoteSerializer, 400: OpenApiResponse(description='File processing error')},
    description='Upload a file (PDF, TXT, MD) and extract text content',
    tags=['Notes']
)
class NoteUploadView(generics.CreateAPIView):
    serializer_class = NoteUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            title = serializer.validated_data.get('title', file.name)
            
            try:
                # Extract text from file
                extracted_text = extract_text_from_file(file)
                cleaned_text = clean_text(extracted_text)
                
                # Create note
                note = Note.objects.create(
                    user=request.user,
                    title=title,
                    original_text=cleaned_text,
                    file=file
                )
                
                return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response(
                    {'error': f'Failed to process file: {str(e)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SummarizeNoteSerializer,
    responses={200: NoteSerializer, 404: OpenApiResponse(description='Note not found')},
    description='Generate AI summary for a specific note',
    tags=['Notes']
)
@api_view(['POST'])
def summarize_note(request, note_id):
    """Generate summary for a specific note"""
    try:
        note = Note.objects.get(id=note_id, user=request.user)
        
        if not note.original_text:
            return Response(
                {'error': 'No text content to summarize'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        method = request.data.get('method', 'huggingface')
        summary = summarize_text(note.original_text, method=method)
        
        # Save summary to note
        note.summary = summary
        note.save()
        
        return Response(NoteSerializer(note).data)
    
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            {'error': f'Summarization failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    request=SummarizeSerializer,
    responses={200: SummaryResponseSerializer, 500: OpenApiResponse(description='Summarization failed')},
    description='Summarize arbitrary text without saving',
    tags=['Notes']
)
@api_view(['POST'])
def summarize_text_view(request):
    """Summarize arbitrary text without saving"""
    serializer = SummarizeSerializer(data=request.data)
    if serializer.is_valid():
        text = serializer.validated_data['text']
        method = serializer.validated_data['method']
        
        try:
            summary = summarize_text(text, method=method)
            return Response({'summary': summary})
        except Exception as e:
            return Response(
                {'error': f'Summarization failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)