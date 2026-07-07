# Roblox Django Project Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Clone the repository
```bash
git clone <repository-url>
cd roblox
```

### 2. Create and activate a virtual environment (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root (you can copy from `.env.example` if available):
```bash
# Copy example file if exists
cp .env.example .env

# Or create a new one
# Add your SECRET_KEY and other environment variables
```

### 5. Run database migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (optional, for admin access)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

- `roblox/` - Main Django project settings
- `people/` - Django app for user management
- `static/` - Static files (CSS, images)
- `db.sqlite3` - SQLite database (created after migrations)

## Key Features

- Django 6.0.5 web framework
- Channels for WebSocket support (WebSocket endpoint: `/ws/status/`)
- WhiteNoise for static file serving
- SQLite database (default, can be changed in settings)

## Notes

- The project uses Django's built-in SQLite database by default
- For production, consider changing to PostgreSQL or MySQL
- Update `ALLOWED_HOSTS` and `DEBUG` settings in production
- Use `python manage.py collectstatic` before deploying to collect static files