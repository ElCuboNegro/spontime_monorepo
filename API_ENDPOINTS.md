# Spontime API Endpoints Documentation

## Overview

This document lists all available API endpoints in the Spontime Django application. The API is built with Django REST Framework (DRF) and follows RESTful conventions.

- **Base URL**: `/api/`
- **Authentication**: Django session authentication (extendable with token authentication)
- **Response Format**: JSON (with GeoJSON support for geographic data)

---

## API Endpoints Summary

The API provides 11 main resource endpoints with 56+ total endpoint operations:

1. **Users** - User account management
2. **Places** - User-created locations with geographic data
3. **Venues** - Partner venue locations
4. **Plans** - Social event/activity planning with proximity search
5. **Attendances** - Track user participation in plans
6. **Join Requests** - Manage requests to join plans
7. **Check-ins** - Location-based check-ins for plans
8. **Messages** - Plan-specific messaging
9. **Clusters** - Geographic groupings of plans (read-only)
10. **Offers** - Venue promotional offers
11. **Recommendations** - Personalized plan recommendations (read-only)

---

## 1. Users API

**Base Path**: `/api/users/`
**Purpose**: Manage user accounts and profiles

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/users/` | List all users with pagination |
| POST | `/api/users/` | Create a new user account |
| GET | `/api/users/{id}/` | Get specific user details |
| PUT | `/api/users/{id}/` | Update user (complete replacement) |
| PATCH | `/api/users/{id}/` | Partially update user fields |
| DELETE | `/api/users/{id}/` | Delete a user account |

**Fields**: `id`, `handle`, `display_name`, `email`, `phone`, `photo_url`, `language`, `status`, `created_at`

---

## 2. Places API

**Base Path**: `/api/places/`
**Purpose**: Manage user-created places/locations with geographic coordinates

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/places/` | List all places (GeoJSON format) |
| POST | `/api/places/` | Create a new place with location |
| GET | `/api/places/{id}/` | Get specific place details |
| PUT | `/api/places/{id}/` | Update place (complete replacement) |
| PATCH | `/api/places/{id}/` | Partially update place fields |
| DELETE | `/api/places/{id}/` | Delete a place |

**Fields**: `id`, `name`, `address`, `city`, `country`, `owner_user`, `tags`, `location` (GeoJSON Point), `created_at`

**Note**: Supports GeoJSON format for geographic data visualization.

---

## 3. Venues API

**Base Path**: `/api/venues/`
**Purpose**: Manage partner venue locations (restaurants, bars, etc.)

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/venues/` | List all venues (GeoJSON format) |
| POST | `/api/venues/` | Create a new venue |
| GET | `/api/venues/{id}/` | Get specific venue details |
| PUT | `/api/venues/{id}/` | Update venue (complete replacement) |
| PATCH | `/api/venues/{id}/` | Partially update venue fields |
| DELETE | `/api/venues/{id}/` | Delete a venue |

**Fields**: `id`, `partner`, `partner_id`, `name`, `address`, `contact`, `categories`, `status`, `location` (GeoJSON Point), `created_at`

**Note**: Supports GeoJSON format for geographic data visualization.

---

## 4. Plans API

**Base Path**: `/api/plans/`
**Purpose**: Manage social events and activities with proximity-based discovery

### Standard Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/plans/` | List all plans with pagination |
| POST | `/api/plans/` | Create a new plan (auto-assigns host) |
| GET | `/api/plans/{id}/` | Get specific plan details |
| PUT | `/api/plans/{id}/` | Update plan (complete replacement) |
| PATCH | `/api/plans/{id}/` | Partially update plan fields |
| DELETE | `/api/plans/{id}/` | Delete a plan |

### Custom Action

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/plans/nearby/` | Find nearby plans based on location |

**Query Parameters for `nearby`**:
- `lat` (required): Latitude coordinate
- `lon` (required): Longitude coordinate
- `radius` (optional): Search radius in meters (default: 5000)

**Fields**: `id`, `host_user`, `venue`, `venue_id`, `place`, `place_id`, `title`, `description`, `tags`, `starts_at`, `ends_at`, `capacity`, `visibility`, `is_active`, `cluster`, `cluster_id`, `rules`, `attendances`, `created_at`, `updated_at`

---

## 5. Attendances API

**Base Path**: `/api/attendances/`
**Purpose**: Track user participation in plans

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/attendances/` | List all attendances (with filters) |
| POST | `/api/attendances/` | Create new attendance record |
| GET | `/api/attendances/{id}/` | Get specific attendance |
| PUT | `/api/attendances/{id}/` | Update attendance (complete replacement) |
| PATCH | `/api/attendances/{id}/` | Partially update attendance |
| DELETE | `/api/attendances/{id}/` | Remove attendance record |

**Query Filters**:
- `plan_id`: Filter by specific plan
- `user_id`: Filter by specific user

**Fields**: `id`, `plan`, `user`, `status`, `joined_at`, `left_at`

---

## 6. Join Requests API

**Base Path**: `/api/join-requests/`
**Purpose**: Manage requests from users to join plans

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/join-requests/` | List all join requests (with filters) |
| POST | `/api/join-requests/` | Create new join request (auto-assigns user) |
| GET | `/api/join-requests/{id}/` | Get specific join request |
| PUT | `/api/join-requests/{id}/` | Update request (complete replacement) |
| PATCH | `/api/join-requests/{id}/` | Partially update request |
| DELETE | `/api/join-requests/{id}/` | Delete join request |

**Query Filters**:
- `plan_id`: Filter by specific plan
- `user_id`: Filter by specific user

**Fields**: `id`, `plan`, `user`, `status`, `created_at`

---

## 7. Check-ins API

**Base Path**: `/api/checkins/`
**Purpose**: Location-based check-ins for plans

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/checkins/` | List all check-ins (with filters) |
| POST | `/api/checkins/` | Create new check-in (auto-assigns user) |
| GET | `/api/checkins/{id}/` | Get specific check-in |
| PUT | `/api/checkins/{id}/` | Update check-in (complete replacement) |
| PATCH | `/api/checkins/{id}/` | Partially update check-in |
| DELETE | `/api/checkins/{id}/` | Delete check-in |

**Query Filters**:
- `user_id`: Filter by specific user
- `plan_id`: Filter by specific plan

**Fields**: `id`, `user`, `plan`, `plan_id`, `geo` (GeoJSON Point), `flags`, `created_at`

---

## 8. Messages API

**Base Path**: `/api/messages/`
**Purpose**: Plan-specific messaging and chat

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/messages/` | List all messages (with filters, ordered by time) |
| POST | `/api/messages/` | Create new message (auto-assigns user) |
| GET | `/api/messages/{id}/` | Get specific message |
| PUT | `/api/messages/{id}/` | Update message (complete replacement) |
| PATCH | `/api/messages/{id}/` | Partially update message |
| DELETE | `/api/messages/{id}/` | Delete message |

**Query Filters**:
- `plan_id`: Filter by specific plan

**Fields**: `id`, `plan`, `user`, `content`, `created_at`

---

## 9. Clusters API (Read-Only)

**Base Path**: `/api/clusters/`
**Purpose**: View geographic groupings of plans

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/clusters/` | List all clusters (GeoJSON format) |
| GET | `/api/clusters/{id}/` | Get specific cluster details |

**Note**: This is a read-only endpoint. Clusters are computed automatically by the system.

**Fields**: `id`, `label`, `scope`, `plan_count`, `centroid` (GeoJSON Point), `created_at`

---

## 10. Offers API

**Base Path**: `/api/offers/`
**Purpose**: Manage promotional offers from venues

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/offers/` | List all offers (with filters) |
| POST | `/api/offers/` | Create new offer |
| GET | `/api/offers/{id}/` | Get specific offer |
| PUT | `/api/offers/{id}/` | Update offer (complete replacement) |
| PATCH | `/api/offers/{id}/` | Partially update offer |
| DELETE | `/api/offers/{id}/` | Delete offer |

**Query Filters**:
- `venue_id`: Filter by specific venue

**Fields**: `id`, `venue`, `venue_id`, `title`, `description`, `valid_from`, `valid_to`, `tags`, `capacity`

---

## 11. Recommendations API (Read-Only)

**Base Path**: `/api/recs/`
**Purpose**: Personalized plan recommendations for users

### Standard Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/recs/` | List all recommendation snapshots |
| GET | `/api/recs/{id}/` | Get specific recommendation snapshot |

### Custom Action

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/recs/feed/` | Get personalized recommendation feed |

**Authentication**: The `/feed/` endpoint requires authentication

**Response Behavior**:
- Returns latest recommendation snapshot for authenticated user
- Returns 200 with message if no recommendations available
- Returns 401 if not authenticated

**Fields**:
- **RecoSnapshot**: `id`, `user`, `generated_at`, `algo_version`, `explanations`, `items`
- **RecoItem**: `id`, `plan`, `score`, `distance_m`, `shared_tags`

---

## Implementation Details

### Source Files

- **URL Configuration**: `spontime/urls.py`, `core/urls.py`
- **Views**: `core/views.py`
- **Serializers**: `core/serializers.py`
- **Models**: `core/models.py`

### Key Features

1. **GeoJSON Support**: Places, Venues, and Clusters return GeoJSON-formatted responses for mapping
2. **Auto-Assignment**: Some endpoints automatically assign the current user (Plans, JoinRequests, CheckIns, Messages)
3. **Filtering**: Multiple endpoints support query parameter filtering for related resources
4. **Pagination**: List endpoints include pagination for large result sets
5. **Custom Actions**: Two custom endpoints for proximity search and personalized recommendations

### CRUD Operations Summary

- **Full CRUD (9 resources)**: Users, Places, Venues, Plans, Attendances, JoinRequests, CheckIns, Messages, Offers
- **Read-Only (2 resources)**: Clusters, Recommendations
- **Total Standard CRUD Endpoints**: 54
- **Total Custom Endpoints**: 2 (nearby, feed)
- **Total Endpoints**: 56+

---

## Next Steps

For API usage examples and integration guides, see:
- Django REST Framework documentation
- OpenAPI/Swagger documentation (if configured)
- Frontend integration examples
