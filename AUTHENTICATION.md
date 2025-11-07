# Authentication Guide

## Overview

Spontime API uses Token Authentication for securing endpoints. This guide explains how to register, login, and use the API.

**Future Enhancement**: Instagram OAuth integration is planned for social authentication.

---

## Authentication Endpoints

### 1. Register (Sign Up)

**Endpoint**: `POST /api/auth/register/`

**Purpose**: Create a new user account and receive an authentication token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "handle": "myusername",
  "password": "securepassword123",
  "display_name": "My Display Name"
}
```

**Response** (201 Created):
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "handle": "myusername",
    "display_name": "My Display Name",
    "email": "user@example.com",
    "phone": null,
    "photo_url": null,
    "language": "en",
    "status": "active",
    "created_at": "2025-11-06T10:30:00Z"
  },
  "message": "User registered successfully"
}
```

**Required Fields**:
- `email` (unique)
- `handle` (unique, case-insensitive)
- `password` (minimum 8 characters, validated)

**Optional Fields**:
- `display_name`
- `phone`
- `photo_url`
- `language` (default: "en")

---

### 2. Login

**Endpoint**: `POST /api/auth/login/`

**Purpose**: Authenticate with existing credentials and receive an authentication token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "handle": "myusername",
    "display_name": "My Display Name",
    "email": "user@example.com",
    "phone": null,
    "photo_url": null,
    "language": "en",
    "status": "active",
    "created_at": "2025-11-06T10:30:00Z"
  },
  "message": "Login successful"
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "Invalid credentials"
}
```

---

### 3. Logout

**Endpoint**: `POST /api/auth/logout/`

**Purpose**: Invalidate the current authentication token.

**Headers Required**:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response** (200 OK):
```json
{
  "message": "Successfully logged out"
}
```

---

### 4. Get Profile

**Endpoint**: `GET /api/auth/profile/`

**Purpose**: Get current authenticated user's profile information.

**Headers Required**:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "handle": "myusername",
  "display_name": "My Display Name",
  "email": "user@example.com",
  "phone": null,
  "photo_url": null,
  "language": "en",
  "status": "active",
  "created_at": "2025-11-06T10:30:00Z"
}
```

---

## Using Authentication Tokens

Once you have a token (from register or login), include it in the `Authorization` header for all authenticated requests:

```
Authorization: Token YOUR_TOKEN_HERE
```

### Example: Create a Plan (Authenticated Request)

```bash
curl -X POST http://localhost:8000/api/plans/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Coffee meetup",
    "description": "Let'\''s grab coffee!",
    "starts_at": "2025-11-07T15:00:00Z",
    "ends_at": "2025-11-07T16:00:00Z",
    "capacity": 5,
    "visibility": "public"
  }'
```

---

## Permission Model

The API uses the following permission model:

### Public Access (No Authentication Required):
- `GET` requests to most resources (read-only)
- `POST /api/auth/register/`
- `POST /api/auth/login/`

### Authenticated Access Required:
- `POST`, `PUT`, `PATCH`, `DELETE` operations on most resources
- Creating plans, messages, check-ins, join requests
- Viewing personalized recommendations (`/api/recs/feed/`)
- `POST /api/auth/logout/`
- `GET /api/auth/profile/`

### Owner-Based Access:
Some endpoints may restrict modifications to resource owners only.

---

## Security Best Practices

1. **Store tokens securely**: Never expose tokens in client-side code or version control
2. **Use HTTPS**: Always use HTTPS in production to encrypt token transmission
3. **Token rotation**: Logout and re-login periodically to refresh tokens
4. **Password requirements**:
   - Minimum 8 characters
   - Cannot be too similar to other personal information
   - Cannot be a commonly used password
   - Cannot be entirely numeric

---

## Error Responses

### 400 Bad Request
Missing or invalid request data.

```json
{
  "email": ["This field is required."],
  "password": ["This field is required."]
}
```

### 401 Unauthorized
Invalid or missing authentication token.

```json
{
  "detail": "Invalid token."
}
```

### 403 Forbidden
Authenticated but lacking permission.

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Testing Authentication

### Using cURL:

**Register**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","handle":"testuser","password":"testpass123"}'
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

**Get Profile**:
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Logout**:
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Migration Notes

Before using authentication, run migrations to create the token table:

```bash
python manage.py migrate
```

---

## Future: Instagram OAuth Integration

The authentication system is designed to accommodate Instagram OAuth in the future:

1. Current token authentication will remain for API access
2. Instagram OAuth will be added as an alternative registration/login method
3. Users will be able to link Instagram accounts to existing Spontime accounts
4. Profile information can be synced from Instagram

**Implementation roadmap**:
- Add Instagram OAuth provider configuration
- Create Instagram callback endpoint
- Link Instagram profiles to User model
- Sync profile photos and display names
- Optional: Import Instagram connections as friend suggestions
