# Spontime

A Django 5 + DRF + PostGIS application with Celery/Redis for scheduled jobs (DBSCAN clustering + recommendations).

**New**: Token-based authentication and Android demo app included!

## Features

- **Django 5** with Django REST Framework (DRF)
- **Token Authentication** with user registration and login
- **PostGIS** for geospatial data and queries
- **Celery + Redis** for scheduled background tasks
- **DBSCAN clustering** using scikit-learn for place grouping
- **Personalized recommendations** based on user check-in history
- **Android Demo App** showcasing authentication and API usage
- **Docker Compose** for easy development and deployment
- **pytest + behave** for testing (unit tests + BDD)
- **pre-commit hooks** for code quality

## Models

- **User**: Custom user model with additional profile fields
- **Place**: Location with PostGIS Point field for geospatial queries
- **Plan**: Event/activity planning with location and participants
- **CheckIn**: User visits to places
- **Cluster**: DBSCAN-generated groups of nearby places
- **Recommendation**: Personalized place suggestions for users

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get authentication token
- `POST /api/auth/logout/` - Logout (invalidate token)
- `GET /api/auth/profile/` - Get current user profile

### Plans
- `GET /api/plans/` - List all plans
- `POST /api/plans/` - Create a new plan (authenticated)
- `GET /api/plans/{id}/` - Get plan details
- `PUT /api/plans/{id}/` - Update a plan
- `DELETE /api/plans/{id}/` - Delete a plan
- `GET /api/plans/nearby/?lat={lat}&lon={lon}&radius={meters}` - Search nearby plans

### Recommendations
- `GET /api/recs/feed/` - Get personalized recommendation feed (authenticated)
- `GET /api/recs/` - List all recommendations

### Other Endpoints
- `GET /api/users/` - List users
- `GET /api/places/` - List places
- `GET /api/checkins/` - List check-ins
- `GET /api/clusters/` - List clusters

**Full API documentation**: See [API_ENDPOINTS.md](./API_ENDPOINTS.md) and [AUTHENTICATION.md](./AUTHENTICATION.md)

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development without Docker)

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd spontime_monorepo
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Build and start services:
```bash
docker-compose up --build
```

4. Run migrations (includes auth token tables):
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the application:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Auth endpoints: http://localhost:8000/api/auth/

7. (Optional) Run the Android demo app:
   - See [android_demo/README.md](./android_demo/README.md) for setup instructions

### Local Development (Without Docker)

1. Install PostgreSQL with PostGIS extension and Redis:
```bash
# On Ubuntu/Debian
sudo apt-get install postgresql-15-postgis-3 redis-server

# On macOS with Homebrew
brew install postgresql@15 postgis redis
```

2. Create a database:
```bash
createdb spontime
psql spontime -c "CREATE EXTENSION postgis;"
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your database and Redis URLs
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Start the development server:
```bash
python manage.py runserver
```

8. In separate terminals, start Celery worker and beat:
```bash
celery -A spontime worker -l info
celery -A spontime beat -l info
```

## Running Tests

### Using pytest
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest core/tests/test_models.py
```

### Using behave (BDD)
```bash
# Run all BDD tests
behave

# Run specific feature
behave features/plans.feature
```

### With Docker
```bash
docker-compose exec web pytest
docker-compose exec web behave
```

## Scheduled Tasks

The application includes two periodic Celery tasks:

1. **Update Clusters** (runs every hour)
   - Groups nearby places using DBSCAN algorithm
   - Creates clusters with centroid and radius information

2. **Generate Recommendations** (runs every 30 minutes)
   - Analyzes user check-in history
   - Creates personalized place recommendations
   - Scores recommendations based on user preferences and proximity

## Code Quality

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pre-commit install
```

Run manually:
```bash
pre-commit run --all-files
```

The hooks will automatically:
- Format code with Black
- Sort imports with isort
- Check code with flake8
- Validate YAML and JSON files
- Check for common issues

## Project Structure

```
spontime_monorepo/
├── spontime/              # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py            # URL configuration
│   └── celery.py          # Celery configuration
├── core/                  # Main application
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── auth_views.py      # Authentication endpoints
│   ├── tasks.py           # Celery tasks
│   ├── admin.py           # Admin configuration
│   └── urls.py            # App URL configuration
├── android_demo/          # Android demo application
│   ├── app/               # Android app source
│   └── README.md          # Android setup guide
├── features/              # BDD tests
│   ├── plans.feature
│   ├── recommendations.feature
│   └── steps/             # Step definitions
├── API_ENDPOINTS.md       # Complete API documentation
├── AUTHENTICATION.md      # Authentication guide
├── docker-compose.yml     # Docker services
├── Dockerfile             # Docker image
├── requirements.txt       # Python dependencies
├── pytest.ini             # Pytest configuration
└── .pre-commit-config.yaml  # Pre-commit hooks
```

## API Examples

### Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "handle": "myusername",
    "password": "securepass123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Create a Place
```bash
curl -X POST http://localhost:8000/api/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "type": "Feature",
    "properties": {
      "name": "Central Park",
      "category": "park",
      "address": "New York, NY"
    },
    "geometry": {
      "type": "Point",
      "coordinates": [-73.965355, 40.782865]
    }
  }'
```

### Create a Plan
```bash
curl -X POST http://localhost:8000/api/plans/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <your-token>" \
  -d '{
    "title": "Picnic in the Park",
    "description": "Let's have a picnic!",
    "place_id": 1,
    "scheduled_time": "2024-12-25T14:00:00Z",
    "status": "active"
  }'
```

### Search Nearby Plans
```bash
curl "http://localhost:8000/api/plans/nearby/?lat=40.7128&lon=-74.0060&radius=5000"
```

### Get Recommendation Feed
```bash
curl http://localhost:8000/api/recs/feed/ \
  -H "Authorization: Token <your-token>"
```

For more examples, see [AUTHENTICATION.md](./AUTHENTICATION.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linters
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
