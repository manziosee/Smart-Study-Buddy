# 🚀 Docker & Dokploy Deployment Guide

## 📋 Prerequisites
- Docker and Docker Compose installed
- Dokploy running on `http://localhost:3000/`
- Git repository access

## 🐳 Docker Setup

### 1. Local Development with Docker
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### 2. Services Included
- **PostgreSQL Database** (port 5432)
- **Redis Cache** (port 6379)
- **Django Web App** (port 8000)
- **Celery Worker** (background tasks)

### 3. Database Migration
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## 🚀 Dokploy Deployment

### 1. Access Dokploy Dashboard
- Open: `http://localhost:3000/`
- Login to your Dokploy instance

### 2. Create New Application
1. Click "New Application"
2. Select "Docker Compose"
3. Fill in details:
   - **Name**: `smart-study-buddy`
   - **Repository**: `https://github.com/manziosee/Smart-Study-Buddy.git`
   - **Branch**: `feature/enhanced-authentication`

### 3. Environment Variables
Set these in Dokploy:
```
DEBUG=False
SECRET_KEY=your_django_secret_key_here
DATABASE_URL=postgresql://postgres:postgres@db:5432/smart_study_buddy
REDIS_URL=redis://redis:6379/0
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Domain Configuration
- **Host**: `smart-study-buddy.local`
- **Port**: `8000`
- **HTTPS**: Enable if needed

### 5. Deploy
1. Click "Deploy"
2. Monitor deployment logs
3. Wait for all services to be healthy

## 🔧 Configuration Files

### Docker Files Created:
- `Dockerfile` - Container definition
- `docker-compose.yml` - Multi-service setup
- `.dockerignore` - Exclude unnecessary files
- `entrypoint.sh` - Container initialization
- `dokploy.json` - Dokploy configuration

### Key Features:
- **PostgreSQL** instead of SQLite
- **Redis** for caching and Celery
- **Gunicorn** for production WSGI
- **Health checks** for database
- **Auto migrations** on startup
- **Static file collection**

## 📊 Service URLs

After deployment:
- **Web App**: `http://smart-study-buddy.local:8000/`
- **API Docs**: `http://smart-study-buddy.local:8000/api/docs/`
- **Admin**: `http://smart-study-buddy.local:8000/admin/`
- **Database**: `localhost:5432` (internal)
- **Redis**: `localhost:6379` (internal)

## 🔍 Monitoring

### Check Service Status
```bash
# View all services
docker-compose ps

# Check logs
docker-compose logs web
docker-compose logs db
docker-compose logs celery

# Execute commands in container
docker-compose exec web python manage.py shell
```

### Health Checks
- Database: `pg_isready -U postgres`
- Web App: `GET /api/analytics/`
- Redis: `redis-cli ping`

## 🛠 Troubleshooting

### Common Issues:
1. **Database Connection**: Check if PostgreSQL is running
2. **Migration Errors**: Run migrations manually
3. **Static Files**: Ensure collectstatic runs
4. **Environment Variables**: Verify all secrets are set

### Debug Commands:
```bash
# Check database connection
docker-compose exec web python manage.py dbshell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic
```

## 🔐 Security Notes

- **SECRET_KEY**: Generated securely
- **Database**: PostgreSQL with persistent volumes
- **Environment**: Production settings enabled
- **ALLOWED_HOSTS**: Configured for Docker
- **Debug**: Disabled in production

## 📈 Performance

- **Gunicorn**: Production WSGI server
- **PostgreSQL**: Optimized database
- **Redis**: Fast caching and task queue
- **Celery**: Background task processing
- **Static Files**: Properly served

Your Smart Study Buddy is now ready for production deployment with Docker and Dokploy! 🎯