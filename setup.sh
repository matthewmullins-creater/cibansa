#!/bin/bash

# Django Startup Script for Cibansa Project
# This script sets up initial data for the Django application

set -e  # Exit on any error

echo "🚀 Starting Django project setup..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the Django project root directory."
    exit 1
fi


echo "🗄️  Running database migrations..."
uv run python manage.py makemigrations
uv run python manage.py migrate

echo "👤 Creating initial data (superuser, courses, articles)..."
uv run python manage.py setup_initial_data --username admin --email admin@boilingfrogs.com --password admin123

echo "📊 Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "✅ Setup completed successfully!"
echo ""
echo "🎉 Your Django application is ready!"
echo ""
echo "📋 Login credentials:"
echo "   Username: admin"
echo "   Email: admin@boilingfrogs.com"
echo "   Password: admin123"
echo ""
echo "🌐 To start the development server, run:"
echo "   uv run python manage.py runserver"
echo ""
echo "🔗 Then visit: http://127.0.0.1:8000"
echo "🔗 Admin panel: http://127.0.0.1:8000/admin"
