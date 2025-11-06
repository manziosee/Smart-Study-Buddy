#!/bin/bash

echo "🧠 Setting up Smart Study Buddy..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create migrations
echo "Creating database migrations..."
python manage.py makemigrations users
python manage.py makemigrations notes
python manage.py makemigrations quizzes

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create superuser (optional)
echo "Would you like to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

echo "✅ Setup complete!"
echo "Run 'python manage.py runserver' to start the development server."
echo "Don't forget to update your .env file with your API keys!"