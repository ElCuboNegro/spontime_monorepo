# Spontime API Documentation

## Overview
The Spontime API enables real-time discovery of spontaneous plans and lightweight chat functionality for plan members.

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently using Django's session authentication. In production, consider adding token-based authentication.

---

## Endpoints

### Plans

#### 1. List All Plans
```
GET /api/plans/
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Quick Coffee at Starbucks",
      "description": "Need a caffeine fix! Anyone want to join?",
      "location_name": "Starbucks, Times Square",
      "start_time": "2025-11-05T18:30:00Z",
      "end_time": "2025-11-05T19:30:00Z",
      "creator": {
        "id": 1,
        "handle": "alice_spontime",
        "photo_url": "https://i.pravatar.cc/150?img=1"
      },
      "tags": [
        {
          "id": 1,
          "name": "Coffee",
          "slug": "coffee"
        }
      ],
      "max_participants": 10,
      "distance": 0.15,
      "member_count": 2
    }
  ]
}
```

#### 2. Get Active Plans (Right Now Feed)
```
GET /api/plans/now/?lat={latitude}&lon={longitude}&radius={km}&tags={tag_ids}
```

**Required Parameters:**
- `lat` (float): User's latitude
- `lon` (float): User's longitude

**Optional Parameters:**
- `radius` (float): Search radius in kilometers (default: 2)
- `tags` (string): Comma-separated tag IDs for filtering (e.g., "1,2,3")

**Example:**
```
GET /api/plans/now/?lat=40.7580&lon=-73.9855&radius=5&tags=1,2
```

**Response:**
Plans are filtered by:
- Active status (`is_active=true`)
- Within specified radius
- Happening now or within next 2 hours
- Matching any of the specified tags (OR logic)

Plans are ordered by:
1. Distance from user location
2. Time proximity to start time

**Response Format:** Same as List All Plans

#### 3. Create a Plan
```
POST /api/plans/
```

**Request Body:**
```json
{
  "title": "Coffee Meetup",
  "description": "Quick coffee at the local cafe",
  "latitude": 40.7580,
  "longitude": -73.9855,
  "location_name": "Blue Bottle Coffee",
  "start_time": "2025-11-05T18:00:00Z",
  "end_time": "2025-11-05T19:00:00Z",
  "tag_ids": [1, 2],
  "max_participants": 5
}
```

**Response:** (201 Created)
Full plan object with creator automatically added as a member.

#### 4. Get Plan Details
```
GET /api/plans/{id}/
```

**Response:**
```json
{
  "id": 1,
  "title": "Quick Coffee at Starbucks",
  "description": "Need a caffeine fix! Anyone want to join?",
  "latitude": 40.7580,
  "longitude": -73.9855,
  "location_name": "Starbucks, Times Square",
  "start_time": "2025-11-05T18:30:00Z",
  "end_time": "2025-11-05T19:30:00Z",
  "creator": {...},
  "members": [{...}, {...}],
  "tags": [{...}],
  "max_participants": 10,
  "is_active": true,
  "created_at": "2025-11-05T17:00:00Z",
  "updated_at": "2025-11-05T17:00:00Z",
  "distance": 0.15,
  "member_count": 2,
  "is_joined": false
}
```

#### 5. Join a Plan
```
POST /api/plans/{id}/join/
```

**Response:** (200 OK)
Full plan object with updated members list.

**Error Responses:**
- 400: Already a member or plan is full
- 401: Authentication required

#### 6. Leave a Plan
```
POST /api/plans/{id}/leave/
```

**Response:** (200 OK)
Full plan object with updated members list.

**Error Responses:**
- 400: Not a member or creator cannot leave
- 401: Authentication required

#### 7. Update a Plan
```
PUT /api/plans/{id}/
PATCH /api/plans/{id}/
```

**Permissions:** Only plan members can update.

#### 8. Delete a Plan
```
DELETE /api/plans/{id}/
```

**Permissions:** Only plan members can delete.

---

### Interest Tags

#### 1. List All Tags
```
GET /api/tags/
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Coffee",
    "slug": "coffee"
  },
  {
    "id": 2,
    "name": "Sports",
    "slug": "sports"
  }
]
```

---

### Messages (Chat)

#### 1. List Messages for a Plan
```
GET /api/plans/{plan_id}/messages/
```

**Permissions:** Only plan members can view messages.

**Response:**
```json
[
  {
    "id": 1,
    "plan": 1,
    "user": {
      "id": 2,
      "handle": "bob_active",
      "photo_url": "https://i.pravatar.cc/150?img=2"
    },
    "content": "I'm in! What time exactly?",
    "created_at": "2025-11-05T17:45:00Z"
  },
  {
    "id": 2,
    "plan": 1,
    "user": {
      "id": 1,
      "handle": "alice_spontime",
      "photo_url": "https://i.pravatar.cc/150?img=1"
    },
    "content": "Let's meet at 3:30 PM!",
    "created_at": "2025-11-05T17:46:00Z"
  }
]
```

#### 2. Post a Message
```
POST /api/plans/{plan_id}/messages/
```

**Permissions:** Only plan members can post messages.

**Rate Limit:** 5 messages per minute per user.

**Request Body:**
```json
{
  "content": "Looking forward to it!"
}
```

**Response:** (201 Created)
```json
{
  "id": 3,
  "plan": 1,
  "user": {
    "id": 2,
    "handle": "bob_active",
    "photo_url": "https://i.pravatar.cc/150?img=2"
  },
  "content": "Looking forward to it!",
  "created_at": "2025-11-05T17:47:00Z"
}
```

**Error Responses:**
- 403: Not a plan member
- 429: Rate limit exceeded (too many messages)

---

## Security & Privacy

### Access Control
- **Chat visibility:** Messages are only visible to plan members (creator + joined users)
- **Posting messages:** Only plan members can post messages
- **Rate limiting:** 5 messages per minute per user to prevent spam

### Privacy
- User data is pseudonymized in API responses (only handle and photo_url exposed)
- No PII (email, full name) is exposed in public endpoints

### Future Enhancements
- WebSocket support for real-time chat (currently polling-based)
- Token-based authentication for mobile apps
- Enhanced geospatial indexing with PostGIS in production

---

## Data Models

### Plan
- `title`: Plan name
- `description`: Plan details
- `latitude`, `longitude`: Location coordinates
- `location_name`: Human-readable location
- `start_time`, `end_time`: Time window
- `creator`: User who created the plan
- `members`: Users who joined
- `tags`: Interest tags for filtering
- `max_participants`: Maximum number of participants
- `is_active`: Whether plan is active

### Message
- `plan`: Associated plan
- `user`: Message author
- `content`: Message text (max 1000 chars)
- `created_at`: Timestamp

### InterestTag
- `name`: Tag name (e.g., "Coffee", "Sports")
- `slug`: URL-friendly version

---

## Example Workflows

### 1. Discover Nearby Plans
```bash
# Get plans near Times Square within 2km
curl "http://localhost:8000/api/plans/now/?lat=40.7580&lon=-73.9855&radius=2"
```

### 2. Filter by Interest
```bash
# Get coffee and sports plans within 5km
curl "http://localhost:8000/api/plans/now/?lat=40.7580&lon=-73.9855&radius=5&tags=1,2"
```

### 3. Join a Plan and Chat
```bash
# 1. Join the plan
curl -X POST http://localhost:8000/api/plans/1/join/ \
  -H "Authorization: Session ..."

# 2. Send a message
curl -X POST http://localhost:8000/api/plans/1/messages/ \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello everyone!"}'

# 3. View messages
curl http://localhost:8000/api/plans/1/messages/
```

---

## Testing

Run the test suite:
```bash
python manage.py test
```

Seed sample data:
```bash
python manage.py seed_data
```

---

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Seed sample data:
```bash
python manage.py seed_data
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run development server:
```bash
python manage.py runserver
```

6. Access admin panel:
```
http://localhost:8000/admin/
```
