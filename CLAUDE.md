# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 5.2.7 application for "Casa Betti Bacheca" - an Italian marketplace/bulletin board for listing items for sale with images, categories, and status tracking.

## Development Commands

### Docker (Recommended)
```bash
# Build and start containers
docker-compose up --build

# Start containers in background
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Execute commands in container
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py shell

# Rebuild container
docker-compose build
```

### Local Development (without Docker)
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files (if deploying)
python manage.py collectstatic
```

### Database
- Uses SQLite (`db.sqlite3`) in development
- Database is already initialized with migrations
- With Docker, database persists in the mounted volume

## Architecture

### Project Structure
- **casa_betti_bacheca/** - Main Django project configuration
  - `settings.py` - Project settings with django-filer and easy-thumbnails configuration
  - `urls.py` - Root URL configuration, includes items app URLs
- **items/** - Main application for item listings
  - `models.py` - Item and ItemImage models with Italian verbose names
  - `views.py` - List, detail views plus JSON API endpoint
  - `admin.py` - Admin configuration with inline image management
  - `templates/items/` - HTML templates using Bootstrap 5 and Alpine.js

### Key Models
- **Item** - Main item model with:
  - Title, description, price (decimal)
  - Category choices (furniture, electronics, clothing, books, sports, other)
  - Status (available, reserved, sold)
  - Timestamps (created_at, updated_at)
  - Italian verbose names throughout

- **ItemImage** - Image model using django-filer:
  - ForeignKey to Item with `related_name='images'`
  - Uses FilerImageField for file management
  - Order field for sorting images
  - First image accessed via `item.main_image` property

### Media & Static Files
- django-filer manages uploaded images in `media/filer_public/` and `media/filer_public_thumbnails/`
- easy-thumbnails configured with high resolution and custom processors
- Static files in `static/` directory
- Bootstrap 5 and Alpine.js loaded from CDN in templates

### API Endpoints
- `/` - Item list page with filtering and search
- `/items/<id>/` - Item detail page
- `/api/items/` - JSON API for items with thumbnail URLs
- `/admin/` - Django admin interface

### Language & Localization
- UI text is in Italian (model verbose names, category/status labels)
- Templates show Italian labels ("Titolo", "Prezzo", "Categoria", etc.)
- Language code set to 'en-us' in settings but content is Italian
