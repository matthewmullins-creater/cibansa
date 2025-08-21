# Cibansa

## Codebase Summary

Cibansa is a full-stack educational content management system built with Django that enables users to create, manage, and consume educational content including articles and courses. The application supports user account management with custom profiles, category-based content organization, topic management, and a comprehensive admin interface with rich text editing capabilities using TinyMCE.

## Backend (Django Application)

**Entry Point:** `manage.py` - Django project management script  
**Main Configuration:** `cibansa/settings.py` - Core Django settings and configuration  
**URL Routing:** `cibansa/urls.py` - Main URL dispatcher  

### App Structure
Django follows an app-based architecture with the following applications:

#### Accounts App (`accounts/`)
- **Purpose:** User authentication, custom user profiles, and account management
- **Models:** Custom User model with email-based authentication, CbUserProfile for extended user information
- **Features:** 
  - Email-based authentication system
  - Custom user profiles with demographic information
  - Profile photo management
  - User visibility controls

#### Main App (`main/`)
- **Purpose:** Core application functionality and shared models
- **Models:** Categories (CbCategory), Topics (CbTopic), Tags (CbTag)
- **Features:**
  - Category management with image uploads
  - Topic organization within categories
  - Tag system for content classification
  - JSON metadata support for extensibility

#### Articles App (`articles/`)
- **Purpose:** Article content management and publishing
- **Models:** Articles (CbArticle) with rich content support
- **Features:**
  - Rich text article creation with TinyMCE integration
  - Category-based article organization
  - Article image management
  - Visibility controls and metadata

#### Courses App (`courses/`)
- **Purpose:** Educational course content management
- **Models:** Courses (CbCourses) with structured learning content
- **Features:**
  - Course creation and management
  - Category-based course organization
  - Course image and content management
  - User-generated course content

### Key Technologies & Integrations
- **Rich Text Editing:** TinyMCE integration for content creation
- **File Management:** Django FileBrowser with Grappelli admin interface
- **Image Processing:** Pillow for image handling and uploads
- **API Framework:** Django REST Framework for API endpoints
- **Database:** PostgreSQL support with SQLite fallback
- **Authentication:** Custom email-based user authentication

## Project Structure

```
cibansa/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                  # SQLite database (development)
├── cibansa/                    # Main project configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI application
├── accounts/                   # User management app
│   ├── models.py               # Custom User and Profile models
│   ├── views.py                # Authentication views
│   ├── serializers.py          # API serializers
│   └── templates/              # Account templates
├── main/                       # Core app with shared models
│   ├── models.py               # Category, Topic, Tag models
│   ├── management/             # Custom management commands
│   │   └── commands/
│   │       └── setup_initial_data.py  # Initial data setup
│   └── templates/              # Main templates
├── articles/                   # Article management app
│   ├── models.py               # Article models
│   ├── views.py                # Article views
│   └── templates/              # Article templates
├── courses/                    # Course management app
│   ├── models.py               # Course models
│   ├── views.py                # Course views
│   └── templates/              # Course templates
└── media/                      # User-uploaded files
    ├── articles/               # Article images
    ├── category/               # Category images
    └── profile-photo/          # User profile photos
```

## Local Setup Instructions

### Prerequisites
- **Python 3.9–3.12** recommended (Django 5.2 compatible)
- **Git** for version control
- **uv** (recommended) or **pip** for package management

**Note:** This project uses Django 5.2.5 and is compatible with Python 3.9 through 3.12. We recommend using Python 3.11 for optimal performance and compatibility.

#### Installing Python 3.11

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**macOS (Homebrew):**
```bash
brew install python@3.11
```

**Windows:**
Download the installer from the [official Python website](https://www.python.org/downloads/).  
During installation, ensure you check "Add Python to PATH".

#### Installing uv (Recommended Package Manager)
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Setup Instructions

#### Method 1: Using uv (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd cibansa

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Run database migrations
uv run python manage.py migrate

# Create initial data (superuser, categories, sample content)
uv run python manage.py setup_initial_data

# Start development server
uv run python manage.py runserver
```

#### Method 2: Traditional Setup
```bash
# Clone the repository
git clone <repository-url>
cd cibansa

# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create initial data
python manage.py setup_initial_data

# Start development server
python manage.py runserver
```

### Initial Data Setup

The project includes a custom management command that creates initial data:

```bash
# Create initial data with default admin user
python manage.py setup_initial_data

# Or customize the admin user
python manage.py setup_initial_data --username admin --email admin@example.com --password yourpassword
```

This command creates:
- 1 superuser with profile
- 5 categories (Programming, Data Science, Web Development, Mobile Development, DevOps)
- 10 tags for content classification
- 10 topics across categories
- 10 sample courses
- 10 sample articles

### Verification

**Application:** http://127.0.0.1:8000/  
**Admin Interface:** http://127.0.0.1:8000/admin/  
**API Endpoints:** http://127.0.0.1:8000/api/ (if configured)

**Test the Setup:**
```bash
# Check if the server is running
curl -I http://127.0.0.1:8000/

# Login to admin with created superuser
# Default credentials: admin@example.com / adminpass123
```

### Development Features

**Admin Interface Enhancements:**
- Grappelli admin theme for improved UI
- FileBrowser for media management
- TinyMCE rich text editor for content creation

**Content Management:**
- Category-based organization
- Rich text content with image uploads
- User profile management with photos
- Tag-based content classification

### Troubleshooting

**Common Issues:**

1. **Database Connection Errors:**
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py migrate
   python manage.py setup_initial_data
   ```

2. **Static Files Issues:**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Errors:**
   ```bash
   # Ensure proper file permissions for media uploads
   chmod 755 media/
   ```

4. **uv Command Not Found:**
   ```bash
   # Install uv first
   pip install uv
   # Or use traditional pip commands
   ```

5. **TinyMCE Not Loading:**
   - Ensure `STATIC_URL` is properly configured in settings
   - Run `python manage.py collectstatic` to collect static files

**Environment Variables:**
The application uses environment variables for production deployment. For development, default settings in `settings.py` are sufficient.

**Database Configuration:**
- Development: SQLite (included)
- Production: PostgreSQL (configure `DATABASE_URL` environment variable)

This setup provides a complete educational content management system with user authentication, rich content creation, and comprehensive admin capabilities.
