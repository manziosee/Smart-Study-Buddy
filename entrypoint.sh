#!/bin/bash

# Wait for database
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U postgres; do
    sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin@example.com', 'admin123', first_name='Admin', last_name='User')
    print('Superuser created: admin@example.com / admin123')
else:
    print('Superuser already exists')
"

# Start server
echo "Starting server..."
exec gunicorn smart_study_buddy.wsgi:application --bind 0.0.0.0:8000 --workers 3