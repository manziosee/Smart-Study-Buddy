from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Note
from .utils.extract_text import extract_text_from_file, clean_text
from .utils.summarize import summarize_text


@login_required
def notes_list(request):
    """List all user notes"""
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/list.html', {'notes': notes})


@login_required
def create_note(request):
    """Create a new note manually"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            note = Note.objects.create(
                user=request.user,
                title=title,
                original_text=content
            )
            messages.success(request, 'Note created successfully!')
            return redirect('note_detail', note_id=note.id)
        else:
            messages.error(request, 'Please provide both title and content.')
    
    return render(request, 'notes/create.html')


@login_required
def upload_file(request):
    """Upload and process a file"""
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        
        if not file:
            messages.error(request, 'Please select a file to upload.')
            return render(request, 'notes/upload.html')
        
        try:
            # Extract text from file
            extracted_text = extract_text_from_file(file)
            cleaned_text = clean_text(extracted_text)
            
            # Create note
            note = Note.objects.create(
                user=request.user,
                title=title or file.name,
                original_text=cleaned_text,
                file=file
            )
            
            messages.success(request, f'File "{file.name}" uploaded and processed successfully!')
            return redirect('note_detail', note_id=note.id)
        
        except Exception as e:
            messages.error(request, f'Failed to process file: {str(e)}')
    
    return render(request, 'notes/upload.html')


@login_required
def note_detail(request, note_id):
    """View note details"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def summarize_note_view(request, note_id):
    """Generate summary for a note"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        if not note.original_text:
            messages.error(request, 'No text content to summarize.')
            return redirect('note_detail', note_id=note.id)
        
        try:
            method = request.POST.get('method', 'huggingface')
            summary = summarize_text(note.original_text, method=method)
            
            note.summary = summary
            note.save()
            
            messages.success(request, 'Summary generated successfully!')
            return redirect('note_detail', note_id=note.id)
        
        except Exception as e:
            messages.error(request, f'Failed to generate summary: {str(e)}')
    
    return render(request, 'notes/summarize.html', {'note': note})