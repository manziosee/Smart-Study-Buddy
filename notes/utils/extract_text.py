import fitz  # PyMuPDF
from pdfminer.high_level import extract_text as pdfminer_extract
import os


def extract_text_from_pdf(file_path):
    """Extract text from PDF using PyMuPDF (fallback to pdfminer)"""
    try:
        # Try PyMuPDF first
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception:
        # Fallback to pdfminer
        try:
            return pdfminer_extract(file_path).strip()
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_file(file):
    """Extract text from uploaded file"""
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension == '.pdf':
        # Save temporarily to extract text
        temp_path = f"/tmp/{file.name}"
        with open(temp_path, 'wb+') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
        
        try:
            text = extract_text_from_pdf(temp_path)
            os.remove(temp_path)  # Clean up
            return text
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
    
    elif file_extension in ['.txt', '.md']:
        # Read text files directly
        return file.read().decode('utf-8')
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


def clean_text(text):
    """Clean and normalize extracted text"""
    # Remove excessive whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)