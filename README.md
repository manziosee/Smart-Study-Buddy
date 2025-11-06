# 🧠 Smart Study Buddy

<div align="center">
  <img src="static/images/favicon.svg" alt="Smart Study Buddy Logo" width="100" height="100">
  <h3>AI-Powered Learning Platform</h3>
  <p>Transform your study materials into interactive summaries and quizzes with artificial intelligence</p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
  [![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
  [![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](https://huggingface.co)
</div>

## ✨ Features

### 🤖 **AI-Powered Core**
- **Smart Summarization**: Generate concise summaries using Hugging Face transformers
- **Quiz Generation**: Create interactive multiple-choice quizzes from your content
- **Text Extraction**: Automatic extraction from PDF, TXT, and Markdown files
- **Groq Integration**: Ultra-fast AI processing (configurable)

### 🎨 **Modern UI/UX**
- **Dark Mode**: System-aware theme with smooth transitions
- **Responsive Design**: Mobile-first approach with touch optimization
- **Interactive Animations**: GSAP-powered smooth animations
- **Particle Effects**: Dynamic background with interactive particles
- **Glass Morphism**: Modern frosted glass design elements
- **Magnetic Buttons**: Cursor-following interactive elements

### 📱 **Cross-Platform**
- **Progressive Web App**: Install as native app on any device
- **Mobile Responsive**: Optimized for phones, tablets, and desktops
- **Touch Friendly**: Gesture-based navigation and interactions
- **Performance Optimized**: Reduced animations on mobile devices

### 🔐 **User Management**
- **Secure Authentication**: Django-based user system
- **Personal Dashboard**: Track notes, summaries, and quiz performance
- **Profile Management**: Customizable user profiles
- **Session Management**: Secure login/logout functionality

### 🛠 **Developer Features**
- **RESTful API**: Complete API with Swagger documentation
- **Admin Interface**: Django admin for content management
- **Database Support**: SQLite (dev) / PostgreSQL (production)
- **Extensible Architecture**: Modular Django app structure

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

## 🖼️ Screenshots

### 🏠 Landing Page
- Beautiful gradient hero section with animated elements
- Interactive particle background
- Responsive design for all devices

### 📋 Dashboard
- Real-time statistics with animated counters
- Quick action cards with hover effects
- Recent activity tracking
- Dark/light theme toggle

### 📄 Notes Management
- Drag-and-drop file upload
- AI-powered summarization
- Interactive note cards
- Mobile-optimized interface

### 🧠 Quiz System
- Auto-generated questions from content
- Interactive quiz interface
- Progress tracking and scoring
- Performance analytics

## 🌐 Live Demo

**Frontend Features:**
- Landing page: `http://127.0.0.1:8000/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Notes: `http://127.0.0.1:8000/notes/`
- Upload: `http://127.0.0.1:8000/notes/upload/`

**API Documentation:**
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- Admin: `http://127.0.0.1:8000/admin/`

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

## 🚀 Performance

### **Frontend Optimizations**
- **Lazy Loading**: Images and components load on demand
- **Code Splitting**: JavaScript bundles optimized for faster loading
- **Mobile Detection**: Reduced animations on mobile devices
- **Caching**: Static assets cached for better performance
- **Compression**: Gzip compression for all text assets

### **Backend Optimizations**
- **Database Indexing**: Optimized queries for faster data retrieval
- **API Caching**: Redis caching for frequently accessed data
- **Background Tasks**: Celery for heavy AI processing
- **Connection Pooling**: Efficient database connections

## 🌍 Browser Support

| Browser | Version | Features |
|---------|---------|----------|
| Chrome | 90+ | ✅ Full support |
| Firefox | 88+ | ✅ Full support |
| Safari | 14+ | ✅ Full support |
| Edge | 90+ | ✅ Full support |
| Mobile Safari | 14+ | ✅ Touch optimized |
| Chrome Mobile | 90+ | ✅ Touch optimized |

**Note**: Advanced animations (particles, magnetic effects) are disabled on mobile devices for better performance.

## 🛡️ Security

- **CSRF Protection**: Django CSRF middleware enabled
- **SQL Injection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping enabled
- **Secure Headers**: Security middleware configured
- **Authentication**: Secure session-based authentication
- **File Upload**: Validated file types and size limits

## Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure PostgreSQL database
3. Set up proper static file serving
4. Configure CORS for frontend integration
5. Set up Celery for background tasks (optional)
6. Enable SSL/HTTPS
7. Configure security headers

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Getting Started**
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/Smart-Study-Buddy.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Add tests for new functionality
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Submit a pull request

### **Development Guidelines**
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add docstrings to functions and classes
- Write tests for new features
- Update documentation as needed

### **Areas for Contribution**
- 🤖 AI model improvements
- 🎨 UI/UX enhancements
- 📱 Mobile optimizations
- 🔍 Bug fixes and performance improvements
- 📝 Documentation updates
- 🌍 Internationalization (i18n)

## 🚀 Roadmap

### **Upcoming Features**
- [ ] Real-time collaboration on notes
- [ ] Voice-to-text note creation
- [ ] Advanced quiz types (fill-in-the-blank, matching)
- [ ] Study streak tracking and gamification
- [ ] Integration with popular note-taking apps
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

### **AI Enhancements**
- [ ] Custom AI model fine-tuning
- [ ] Multi-modal content support (images, videos)
- [ ] Personalized learning recommendations
- [ ] Adaptive difficulty in quizzes
- [ ] Natural language query interface

## 📜 Documentation

- **API Documentation**: Available at `/api/docs/` when running the server
- **User Guide**: Comprehensive guides in the `/docs/` directory
- **Developer Docs**: Technical documentation for contributors
- **Deployment Guide**: Step-by-step production deployment

## 🙏 Acknowledgments

- **Hugging Face**: For providing excellent AI models and transformers library
- **Django**: For the robust web framework
- **TailwindCSS**: For the utility-first CSS framework
- **GSAP**: For smooth animations and interactions
- **Particles.js**: For beautiful particle effects
- **Font Awesome**: For the comprehensive icon library

## 📞 Support

Need help? Here's how to get support:

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Submit an enhancement issue
- 💬 **Questions**: Start a discussion on GitHub
- 📧 **Security Issues**: Email security@smartstudybuddy.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Made with ❤️ by the Smart Study Buddy team</p>
  <p>🌟 Star this repo if you find it helpful!</p>
</div>