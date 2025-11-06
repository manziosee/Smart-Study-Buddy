#!/bin/bash

echo "🐳 Setting up Smart Study Buddy with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your actual API keys before running docker-compose up"
fi

# Build and start services
echo "🚀 Building and starting services..."
docker-compose up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123', first_name='Admin', last_name='User')
    print('✅ Superuser created: admin@example.com / admin123')
else:
    print('ℹ️  Superuser already exists')
"

echo "🎉 Setup complete!"
echo "📱 Web App: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs/"
echo "🔧 Admin: http://localhost:8000/admin/"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"