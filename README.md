# 🧠 Smart Study Buddy

AI-powered app that helps learners summarize notes, understand concepts, and generate quizzes instantly.

## Features

- **File Upload**: Upload PDF, text, and markdown files
- **Text Extraction**: Automatic text extraction from uploaded documents
- **AI Summarization**: Generate concise summaries using Hugging Face models
- **Quiz Generation**: Create interactive quizzes from your study materials
- **User Dashboard**: Track your notes, summaries, and quiz attempts
- **RESTful API**: Complete API for all functionality

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI Models**: Hugging Face Transformers
- **File Processing**: PyMuPDF, pdfminer.six
- **Authentication**: Django Auth

## Quick Start

### 1. Setup Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Git Bash (Windows):
source venv/Scripts/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Copy `.env` file and update with your API keys:

```bash
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` for admin interface.
Visit `http://127.0.0.1:8000/api/docs/` for Swagger API documentation.
Visit `http://127.0.0.1:8000/api/redoc/` for ReDoc API documentation.

## API Documentation

The API is fully documented with Swagger/OpenAPI:

- **Swagger UI**: `http://127.0.0.1:8000/api/docs/` - Interactive API documentation
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/` - Alternative documentation view
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/` - Raw OpenAPI schema

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - User profile

### Notes
- `GET /api/notes/` - List user notes
- `POST /api/notes/` - Create new note
- `GET /api/notes/{id}/` - Get specific note
- `POST /api/upload/` - Upload file and extract text
- `POST /api/notes/{id}/summarize/` - Generate summary
- `POST /api/summarize/` - Summarize arbitrary text

### Quizzes
- `GET /api/quizzes/` - List user quizzes
- `GET /api/quizzes/{id}/` - Get specific quiz
- `POST /api/quiz/generate/` - Generate quiz from note
- `POST /api/quiz/submit/` - Submit quiz answers
- `GET /api/quiz/attempts/` - List quiz attempts

## Usage Examples

### Upload and Summarize a Document

```bash
# Upload file
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "title=My Study Notes"

# Generate summary
curl -X POST http://localhost:8000/api/notes/1/summarize/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"method": "huggingface"}'
```

### Generate and Take a Quiz

```bash
# Generate quiz
curl -X POST http://localhost:8000/api/quiz/generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"note_id": 1, "num_questions": 5}'

# Submit quiz answers
curl -X POST http://localhost:8000/api/quiz/submit/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"quiz_id": 1, "answers": {"1": "Answer A", "2": "Answer B"}}'
```

## Project Structure

```
smart_study_buddy/
├── manage.py
├── requirements.txt
├── smart_study_buddy/          # Project settings
├── users/                      # User management
├── notes/                      # File upload & summarization
│   └── utils/                  # Text extraction & AI utilities
├── quizzes/                    # Quiz generation & management
│   └── utils/                  # Quiz generation utilities
├── static/                     # Static files
├── media/                      # Uploaded files
└── templates/                  # HTML templates
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure PostgreSQL database
3. Set up proper static file serving
4. Configure CORS for frontend integration
5. Set up Celery for background tasks (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.