# API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Chat API](#chat-api)
3. [FIR Management API](#fir-management-api)
4. [Legal Database API](#legal-database-api)
5. [User Management API](#user-management-api)
6. [WebSocket API](#websocket-api)
7. [Error Handling](#error-handling)

## Authentication

### JWT Authentication
All API endpoints require JWT (JSON Web Token) authentication except for login and registration.

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "email": "officer@police.gov.in",
    "password": "your_password"
}
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer {refresh_token}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer {access_token}
```

## Chat API

### Start Conversation
```http
POST /api/chat/start
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "user_id": "officer_123",
    "session_id": "session_xyz"
}
```

### Send Message
```http
POST /api/chat/message
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "message": "What is IPC section 302?",
    "session_id": "session_xyz",
    "timestamp": "2024-03-15T10:30:00Z"
}
```

### Get Chat History
```http
GET /api/chat/history/{session_id}
Authorization: Bearer {access_token}
```

## FIR Management API

### Create FIR
```http
POST /api/fir/create
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "complainant": {
        "name": "John Doe",
        "contact": "9876543210",
        "address": "123 Main St, City"
    },
    "incident": {
        "date": "2024-03-15",
        "time": "14:30",
        "location": "Park Street",
        "description": "Detailed incident description"
    },
    "sections": ["IPC 302", "IPC 34"],
    "witnesses": [
        {
            "name": "Jane Smith",
            "contact": "9876543211"
        }
    ]
}
```

### Update FIR Status
```http
PUT /api/fir/{fir_id}/status
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "status": "under_investigation",
    "remarks": "Investigation in progress"
}
```

### Get FIR Details
```http
GET /api/fir/{fir_id}
Authorization: Bearer {access_token}
```

### List FIRs
```http
GET /api/fir/list
Authorization: Bearer {access_token}
Query Parameters:
- status
- date_from
- date_to
- page
- limit
```

### Generate FIR Document
```http
POST /api/fir/{fir_id}/generate
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "format": "pdf",
    "include_attachments": true
}
```

## Legal Database API

### Search IPC Sections
```http
GET /api/ipc/search
Authorization: Bearer {access_token}
Query Parameters:
- query
- section_number
- category
- page
- limit
```

### Get Section Details
```http
GET /api/ipc/section/{section_number}
Authorization: Bearer {access_token}
```

### Get Related Sections
```http
GET /api/ipc/section/{section_number}/related
Authorization: Bearer {access_token}
```

### Get Case Precedents
```http
GET /api/ipc/section/{section_number}/precedents
Authorization: Bearer {access_token}
```

## User Management API

### Create User
```http
POST /api/users/create
Authorization: Bearer {admin_token}
Content-Type: application/json

{
    "email": "officer@police.gov.in",
    "name": "Officer Name",
    "department": "Crime Branch",
    "badge_number": "PB123456",
    "role": "investigating_officer"
}
```

### Update User Profile
```http
PUT /api/users/{user_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "Updated Name",
    "contact": "9876543210",
    "department": "Special Branch"
}
```

### Get User Profile
```http
GET /api/users/{user_id}
Authorization: Bearer {access_token}
```

## WebSocket API

### Connect
```javascript
const socket = new WebSocket('ws://api.example.com/ws');
socket.onopen = () => {
    socket.send(JSON.stringify({
        type: 'auth',
        token: 'your_access_token'
    }));
};
```

### Real-time Chat Events
```javascript
// Send message
socket.send(JSON.stringify({
    type: 'message',
    content: 'Hello',
    session_id: 'session_xyz'
}));

// Receive message
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'message') {
        console.log('New message:', data.content);
    }
};
```

### FIR Update Notifications
```javascript
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'fir_update') {
        console.log('FIR Update:', data.fir_id, data.status);
    }
};
```

## Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {
            "field": "Additional error details"
        }
    }
}
```

### Common Error Codes
- `AUTH_001`: Authentication failed
- `AUTH_002`: Token expired
- `AUTH_003`: Invalid token
- `FIR_001`: Invalid FIR data
- `FIR_002`: FIR not found
- `IPC_001`: Section not found
- `USR_001`: User not found
- `VAL_001`: Validation error

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Unprocessable Entity
- `429`: Too Many Requests
- `500`: Internal Server Error

## Rate Limiting

API requests are limited to:
- 100 requests per minute for regular endpoints
- 1000 requests per day for document generation
- 50 concurrent WebSocket connections per user

Rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1583850000
```

## API Versioning

The API is versioned through the URL:
```http
https://api.example.com/v1/endpoint
```

Current stable version: `v1`
Beta version: `v2-beta`

## Security Recommendations

1. Always use HTTPS
2. Keep access tokens secure
3. Implement token refresh mechanism
4. Use strong passwords
5. Monitor API usage
6. Implement request signing for sensitive operations

## Support

For API support:
- Email: api-support@legalai-assistant.org
- Documentation: https://docs.legalai-assistant.org
- Status page: https://status.legalai-assistant.org 