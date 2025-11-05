# spontime_monorepo

Spontime - Spontaneous hangout discovery platform enabling users to discover nearby active plans, filter by interests, and chat with plan members in real-time.

## Features

- 🗺️ **Location-based discovery**: Find plans happening near you right now
- 🏷️ **Interest filtering**: Filter plans by tags (coffee, sports, food, etc.)
- 💬 **Lightweight chat**: Exchange messages with plan members
- 🔒 **Privacy-focused**: Chat visible only to plan members
- ⚡ **Rate-limited**: Anti-spam protection (5 messages/min/user)

## Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ElCuboNegro/spontime_monorepo.git
cd spontime_monorepo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Seed sample data (optional):
```bash
python manage.py seed_data
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## API Documentation

See [API_DOCS.md](API_DOCS.md) for detailed API documentation.

### Key Endpoints

- `GET /api/plans/now/` - Get active plans near you
- `POST /api/plans/` - Create a new plan
- `POST /api/plans/{id}/join/` - Join a plan
- `GET /api/plans/{plan_id}/messages/` - View plan messages
- `POST /api/plans/{plan_id}/messages/` - Send a message

### Example: Discover Nearby Plans

```bash
curl "http://localhost:8000/api/plans/now/?lat=40.7580&lon=-73.9855&radius=2"
```

## Running Tests

```bash
python manage.py test
```

## Architecture

### Apps
- **users**: Custom user model with location support
- **plans**: Plan creation, discovery, and management
- **chat**: Lightweight messaging for plan members

### Key Models
- **User**: Extended Django user with handle, photo, and location
- **Plan**: Spontaneous events with location, time, and tags
- **InterestTag**: Categories for filtering plans
- **Message**: Chat messages linked to plans

### Technology Stack
- Django 4.2
- Django REST Framework
- Django Channels (WebSocket support)
- SQLite (development) / PostgreSQL (production recommended)
- Haversine formula for distance calculations

## Security & Privacy

- Chat messages visible only to plan members
- Rate limiting prevents spam (5 msg/min/user)
- User data pseudonymized (only handle/photo exposed)
- No PII exposure in public endpoints

## Future Enhancements

- WebSocket support for real-time chat
- PostGIS for enhanced geospatial queries
- Mobile app with token authentication
- Push notifications for plan updates
- Advanced search and filtering

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.