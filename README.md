# Spontime

A full-stack monorepo for a location-based social planning platform.

## Architecture

This is a monorepo containing:
- **Backend**: Django 5 + DRF + PostGIS with Celery/Redis for scheduled jobs
- **Frontend**: Modern web application for user interfaces (implementation TBD)

## Features

- **Django 5** with Django REST Framework (DRF)
- **PostGIS** for geospatial data and queries
- **Celery + Redis** for scheduled background tasks
- **DBSCAN clustering** using scikit-learn for place grouping
- **Personalized recommendations** based on user check-in history
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

### Plans
- `GET /api/plans/` - List all plans
- `POST /api/plans/` - Create a new plan
- `GET /api/plans/{id}/` - Get plan details
- `PUT /api/plans/{id}/` - Update a plan
- `DELETE /api/plans/{id}/` - Delete a plan
- `GET /api/plans/nearby/?lat={lat}&lon={lon}&radius={meters}` - Search nearby plans

### Recommendations
- `GET /api/recs/feed/` - Get personalized recommendation feed for authenticated user
- `GET /api/recs/` - List all recommendations

### Other Endpoints
- `GET /api/users/` - List users
- `GET /api/places/` - List places
- `GET /api/checkins/` - List check-ins
- `GET /api/clusters/` - List clusters

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
cp backend/.env.example backend/.env
```

3. Build and start services:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec backend python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. Access the application:
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Frontend: http://localhost:3000/ (when implemented)

### Local Development (Without Docker)

#### Backend

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
cd backend
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

#### Frontend

See [frontend/README.md](frontend/README.md) for frontend setup instructions.

## Running Tests

### Backend Tests

#### Using pytest
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=html

# Run specific test file
pytest core/tests/test_models.py
```

#### Using behave (BDD)
```bash
cd backend

# Run all BDD tests
behave

# Run specific feature
behave features/plans.feature
```

#### With Docker
```bash
docker-compose exec backend pytest
docker-compose exec backend behave
```

### Frontend Tests

See [frontend/README.md](frontend/README.md) for frontend testing instructions.

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
├── backend/                      # Backend Django application
│   ├── spontime/                 # Django project settings
│   │   ├── settings.py           # Main settings file
│   │   ├── urls.py               # URL configuration
│   │   └── celery.py             # Celery configuration
│   ├── core/                     # Main application
│   │   ├── models.py             # Database models
│   │   ├── serializers.py        # DRF serializers
│   │   ├── views.py              # API views
│   │   ├── tasks.py              # Celery tasks
│   │   ├── admin.py              # Admin configuration
│   │   └── urls.py               # App URL configuration
│   ├── features/                 # BDD tests
│   │   ├── plans.feature
│   │   ├── recommendations.feature
│   │   └── steps/                # Step definitions
│   ├── docker-compose.yml        # Backend Docker services
│   ├── Dockerfile                # Backend Docker image
│   ├── requirements.txt          # Python dependencies
│   ├── pytest.ini                # Pytest configuration
│   ├── API.md                    # API documentation
│   └── .pre-commit-config.yaml   # Pre-commit hooks
├── frontend/                     # Frontend application
│   ├── src/                      # Source code
│   ├── features/                 # BDD feature files
│   │   ├── authentication.feature
│   │   ├── plans.feature
│   │   ├── recommendations.feature
│   │   ├── places.feature
│   │   ├── clusters.feature
│   │   └── profile.feature
│   ├── public/                   # Static assets
│   ├── tests/                    # Frontend tests
│   └── README.md                 # Frontend documentation
├── docker-compose.yml            # Root Docker Compose (orchestrates both)
├── README.md                     # This file
└── LICENSE                       # MIT License
```

## API Examples

### Create a Place
```bash
curl -X POST http://localhost:8000/api/places/ \
  -H "Content-Type: application/json" \
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linters
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
