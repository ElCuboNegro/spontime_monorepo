# API Documentation

## Base URL
All API endpoints are prefixed with `/api/`

## Authentication
Currently, the API uses Django's session authentication. Token authentication can be added by configuring DRF's TokenAuthentication.

## Endpoints

### Users

#### List Users
```http
GET /api/users/
```

Response:
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Love exploring new places!",
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

### Places

#### List Places
```http
GET /api/places/
```

Response (GeoJSON):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "geometry": {
        "type": "Point",
        "coordinates": [-73.965355, 40.782865]
      },
      "properties": {
        "name": "Central Park",
        "description": "Large public park in NYC",
        "address": "New York, NY",
        "category": "park",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
      }
    }
  ]
}
```

#### Create Place
```http
POST /api/places/
Content-Type: application/json
```

Request Body (GeoJSON):
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-73.965355, 40.782865]
  },
  "properties": {
    "name": "Central Park",
    "description": "Large public park in NYC",
    "address": "New York, NY",
    "category": "park"
  }
}
```

### Plans

#### List Plans
```http
GET /api/plans/
```

Response:
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/plans/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Picnic in Central Park",
      "description": "Let's enjoy a sunny day!",
      "creator": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "",
        "created_at": "2024-01-01T12:00:00Z"
      },
      "place": {
        "type": "Feature",
        "id": 1,
        "geometry": {
          "type": "Point",
          "coordinates": [-73.965355, 40.782865]
        },
        "properties": {
          "name": "Central Park",
          "category": "park",
          "address": "New York, NY",
          "created_at": "2024-01-01T12:00:00Z"
        }
      },
      "participants": [],
      "scheduled_time": "2024-12-25T14:00:00Z",
      "status": "active",
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

#### Create Plan
```http
POST /api/plans/
Content-Type: application/json
Authorization: Token <your-token>
```

Request Body:
```json
{
  "title": "Picnic in Central Park",
  "description": "Let's enjoy a sunny day!",
  "place_id": 1,
  "participant_ids": [2, 3],
  "scheduled_time": "2024-12-25T14:00:00Z",
  "status": "active"
}
```

#### Search Nearby Plans
```http
GET /api/plans/nearby/?lat=40.7128&lon=-74.0060&radius=5000
```

Query Parameters:
- `lat` (required): Latitude
- `lon` (required): Longitude  
- `radius` (optional): Search radius in meters (default: 5000)

Response: Same format as List Plans

### Check-Ins

#### List Check-Ins
```http
GET /api/checkins/
```

Optional query parameters:
- `user_id`: Filter by user ID

Response:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "",
        "created_at": "2024-01-01T12:00:00Z"
      },
      "place": {
        "type": "Feature",
        "id": 1,
        "geometry": {
          "type": "Point",
          "coordinates": [-73.965355, 40.782865]
        },
        "properties": {
          "name": "Central Park",
          "category": "park"
        }
      },
      "timestamp": "2024-01-15T10:30:00Z",
      "notes": "Great place for a morning jog!"
    }
  ]
}
```

#### Create Check-In
```http
POST /api/checkins/
Content-Type: application/json
Authorization: Token <your-token>
```

Request Body:
```json
{
  "place_id": 1,
  "plan_id": 2,
  "notes": "Great place!"
}
```

### Clusters

#### List Clusters
```http
GET /api/clusters/
```

Response (GeoJSON):
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": 1,
      "geometry": {
        "type": "Point",
        "coordinates": [-73.965, 40.782]
      },
      "properties": {
        "cluster_id": 0,
        "places": [...],
        "place_count": 5,
        "radius": 850.5,
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T13:00:00Z"
      }
    }
  ]
}
```

### Recommendations

#### Get Recommendation Feed
```http
GET /api/recs/feed/
Authorization: Token <your-token>
```

Response:
```json
[
  {
    "id": 1,
    "place": {
      "type": "Feature",
      "id": 5,
      "geometry": {
        "type": "Point",
        "coordinates": [-73.970, 40.780]
      },
      "properties": {
        "name": "New Coffee Shop",
        "category": "cafe",
        "address": "123 Main St, NY"
      }
    },
    "score": 0.85,
    "reason": "You've visited 3 cafe places. Near places you like",
    "created_at": "2024-01-15T12:00:00Z"
  }
]
```

#### List All Recommendations
```http
GET /api/recs/
```

Response: Same format as feed, but includes recommendations for all users

## Error Responses

### 400 Bad Request
```json
{
  "error": "lat and lon parameters are required"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Pagination

List endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of results per page (default: 20, max: 100)

## GeoJSON Format

Endpoints dealing with geographic data (Places, Clusters) use GeoJSON format:
- Points are represented as `[longitude, latitude]` (note the order!)
- SRID is always 4326 (WGS 84)

## Celery Tasks

The following background tasks run automatically:

### Update Clusters
- **Frequency**: Every hour
- **Task**: `core.tasks.update_clusters`
- **Description**: Groups nearby places using DBSCAN algorithm

### Generate Recommendations  
- **Frequency**: Every 30 minutes
- **Task**: `core.tasks.generate_recommendations`
- **Description**: Creates personalized place recommendations based on user check-in history

You can also trigger these tasks manually:
```python
from core.tasks import update_clusters, generate_recommendations

# Trigger tasks
update_clusters.delay()
generate_recommendations.delay()
```
