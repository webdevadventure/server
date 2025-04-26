# Real Estate Management System

A Django-based real estate management system with features for property listing, user management, transactions, and more.

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database:
- Create a PostgreSQL database
- Update database settings in `core/settings.py` with your credentials:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'your_db_name',
          'USER': 'your_db_user',
          'PASSWORD': 'your_db_password',
          'HOST': 'localhost',
          'PORT': '5432',
      }
  }
  ```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Project Structure

The project consists of the following apps:

- `user_mgmt`: User management and authentication
- `location`: Location management (provinces, cities, districts, etc.)
- `listing`: Property listings and reviews
- `transaction`: Payment and transaction management
- `blog`: Blog posts and comments
- `admin_custom`: Custom admin functionalities

## API Endpoints

API documentation will be available at `/api/docs/` after setting up drf-spectacular (coming soon). 