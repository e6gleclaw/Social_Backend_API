# Social Backend API

A FastAPI-based social media backend API with user authentication, friend management, and profile features.

## Features

- User registration and authentication
- JWT-based secure login
- User profile management
- Friend request system
- Friend suggestions
- User search with pagination
- List users with pagination

## Tech Stack

- FastAPI
- MySQL
- SQLAlchemy ORM
- JWT Authentication
- Pydantic for data validation
- Python 3.8+

## Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd social-backend-api
```

2. Create and activate virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the root directory with:

```
DATABASE_URL="mysql+pymysql://username:yourpassword@localhost:3306/db_name"
JWT_SECRET_KEY="your-secret-key"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Set up the database:

```bash
python -m app.tests.setup_db
```

6. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

### Authentication

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "full_name": "string"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username: string
password: string
```

### User Management

#### Get Current User Profile

```http
GET /users/me
Authorization: Bearer <token>
```

#### Update Profile

```http
PUT /users/me
Authorization: Bearer <token>
Content-Type: application/json

{
    "full_name": "string",
    "bio": "string"
}
```

#### List Users (Paginated)

```http
GET /users?page=1&page_size=10
Authorization: Bearer <token>
```

#### Search Users

```http
GET /users/search?query=string&page=1&page_size=10
Authorization: Bearer <token>
```

### Friend Management

#### Send Friend Request

```http
POST /friends/request
Authorization: Bearer <token>
Content-Type: application/json

{
    "friend_id": integer
}
```

#### Accept/Reject Friend Request

```http
PUT /friends/request/{request_id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "accepted" | "rejected"
}
```

#### List Friend Requests

```http
GET /friends/requests
Authorization: Bearer <token>
```

#### List Friends

```http
GET /friends
Authorization: Bearer <token>
```

#### Get Friend Suggestions

```http
GET /friends/suggestions
Authorization: Bearer <token>
```

## Testing

Run tests:

```bash
pytest app/tests/
```

## API Response Examples

### Successful Response

```json
{
  "status": "success",
  "data": {
    // Response data
  }
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Error message"
}
```

## Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS enabled
- Input validation
- SQL injection prevention

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
