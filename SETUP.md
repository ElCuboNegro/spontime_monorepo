# Development Setup Guide

This guide helps you set up the Spontime monorepo for development with all quality gates enabled.

## Prerequisites

- Python 3.12+
- Node.js 18+ (for frontend, when implemented)
- Docker and Docker Compose
- Git

## Quick Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd spontime_monorepo
```

### 2. Install Quality Gates Tools

Install the root-level quality tools (pre-commit, linters, etc.):

```bash
pip install -r requirements.txt
```

For additional development tools:

```bash
pip install -r requirements-dev.txt
```

### 3. Install Pre-commit Hooks

**REQUIRED** per Constitution Principle VI:

```bash
pre-commit install
```

This installs git hooks that will:
- Format code with Black
- Sort imports with isort
- Lint with flake8
- Run pytest on Python file changes
- Validate YAML/JSON files

### 4. Test Pre-commit Setup

```bash
# Run hooks on all files to ensure everything works
pre-commit run --all-files
```

## Backend Setup

### Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Database Setup (Docker)

```bash
# Start PostgreSQL with PostGIS and Redis
docker-compose up -d db redis

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate sample data (optional)
python manage.py generate_sample_data
```

### Run Backend Tests

**REQUIRED before any PR** per Constitution Pre-Merge Requirements:

```bash
cd backend

# Unit tests
pytest

# BDD tests
behave

# With coverage
pytest --cov=core --cov-report=html
```

### Run Backend Server

```bash
cd backend
python manage.py runserver
```

Access at: http://localhost:8000

## Frontend Setup (React Native)

> **Note**: React Native setup is pending. See [frontend/README.md](frontend/README.md) for future instructions.

Once implemented:

```bash
cd frontend

# Install dependencies
npm install

# Run tests
npm test

# Run linter
npm run lint

# Type check
npx tsc --noEmit
```

## Docker Setup (Full Stack)

### Start All Services

```bash
# From repository root
docker-compose up --build
```

Services:
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Run Migrations in Docker

```bash
docker-compose exec backend python manage.py migrate
```

### Run Tests in Docker

```bash
# Unit tests
docker-compose exec backend pytest

# BDD tests
docker-compose exec backend behave
```

## Quality Gates Validation

### Pre-commit Hooks (Local)

Runs automatically on `git commit`:

✅ Black (Python formatter)
✅ isort (import sorting)
✅ flake8 (linting)
✅ pytest (on Python file changes)

### CI Pipeline (GitHub Actions)

Runs automatically on push/PR:

✅ pytest (all unit tests)
✅ behave (all BDD tests)
✅ docker-compose build backend

**All must pass before PR merge** per Constitution v1.3.0.

## Common Commands

### Pre-commit

```bash
# Run hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Skip hooks (NOT RECOMMENDED)
git commit --no-verify  # Only for emergencies!
```

### Testing

```bash
# Backend unit tests
cd backend && pytest

# Backend BDD tests
cd backend && behave

# Run specific test file
cd backend && pytest core/tests/test_models.py

# Run with coverage
cd backend && pytest --cov=core --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Code Quality

```bash
# Format all Python files
black backend/

# Sort imports
isort backend/

# Lint
flake8 backend/

# Type check (if using mypy)
mypy backend/
```

### Docker

```bash
# Build services
docker-compose build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Clean everything
docker-compose down -v
```

## Branch Strategy (Gitflow)

Per Constitution v1.3.0:

```bash
# Create feature branch from develop
git checkout develop
git pull
git checkout -b 001-feature-name

# Make changes and commit
git add .
git commit -m "feat: add feature"

# Push and create PR
git push origin 001-feature-name
```

**Protected Branches:**
- `main` - Production ready, no direct commits
- `develop` - Integration branch, no direct commits

All changes via Pull Request with:
- ✅ CI passing (tests + build)
- ✅ Code review approval
- ✅ Constitution compliance

## Troubleshooting

### Pre-commit Hooks Failing

```bash
# Update hooks to latest versions
pre-commit autoupdate

# Clean and reinstall
pre-commit clean
pre-commit install
```

### Database Connection Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d db
cd backend && python manage.py migrate
```

### Port Already in Use

```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000    # Windows
```

## Constitution Compliance Checklist

Before submitting PR:

- [ ] Pre-commit hooks installed and passing
- [ ] All backend unit tests pass (`pytest`)
- [ ] All backend BDD tests pass (`behave`)
- [ ] Backend Docker build succeeds (`docker-compose build backend`)
- [ ] Feature has clear business/UX impact (Principle VII)
- [ ] Code follows Gitflow workflow
- [ ] PR references feature specification
- [ ] No secrets committed (.env files)

## Resources

- [Constitution](.specify/memory/constitution.md) - Project principles and requirements
- [Backend API Documentation](backend/API.md)
- [Contributing Guide](CONTRIBUTING.md) - Coming soon
- [CI/CD Pipeline](.github/workflows/ci.yml)

## Support

For questions or issues:
1. Check this guide
2. Review the Constitution
3. Ask in team chat
4. Create an issue on GitHub
