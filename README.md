# FastAPI Todo Backend API

A feature-rich todo list backend API built with FastAPI, featuring JWT authentication and MongoDB storage.

## Features
- User authentication with JWT tokens
- Todo list management
- Multiple todo lists per user
- MongoDB integration
- RESTful API design
- API documentation with Swagger UI
- Secure password hashing with bcrypt
- CORS support for frontend integration

## Project Structure
```
your_project/
├── backend/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and router configuration
│   ├── auth.py          # JWT authentication logic
│   ├── database.py      # MongoDB functions
│   ├── models.py        # Pydantic models
│   ├── utils.py         # Utility functions
│   └── routes/
│       ├── __init__.py
│       ├── auth.py      # Authentication endpoints
│       ├── todos.py     # Todo management endpoints
│       └── lists.py     # List management endpoints
├── requirements.txt
└── .env                 # Environment variables
```

## Setup
1. Clone this repository

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
MONGODB_URI=your_mongodb_connection_string
SECRET_KEY=your_jwt_secret_key
```

4. Start the server:
```bash
uvicorn backend.main:app --reload
```

## API Documentation
Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get access token

### Todo Lists
- `GET /lists` - Get user's todo lists
- `POST /lists` - Create new todo list

### Todos
- `GET /todos` - Get all todos
- `POST /todos` - Create new todo
- `GET /todos/{list_id}` - Get todos for specific list
- `POST /todos/{list_id}` - Create todo in specific list

## Authentication
The API uses JWT tokens for authentication:

1. Register a new user or login to get an access token
2. Include the token in subsequent requests:
```http
Authorization: Bearer <your_access_token>
```

## Database Schema

### Users
- username (string)
- email (string)
- hashed_password (string)
- full_name (string)

### Lists
- name (string)
- description (string, optional)
- user_id (string)
- created_at (datetime)

### Todos
- title (string)
- completed (boolean)
- list_id (string)
- user_id (string)
- created_at (datetime)

## Development
Built with:
- FastAPI
- MongoDB
- PyJWT
- Pydantic
- Python-dotenv
- Bcrypt

## CORS Configuration
The API is configured to accept requests from:
- http://localhost:3000 (React/Next.js frontend)
- http://localhost:8000 (FastAPI docs)

## Error Handling
The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Security Features

1. Password Hashing
   - Passwords are hashed using bcrypt
   - Implemented in utils.py

2. JWT Authentication
   - 30-minute token expiration
   - Secure token validation
   - Protected routes using FastAPI dependencies

3. MongoDB Security
   - Indexed collections for performance
   - Proper data isolation between users
   - Secure connection string handling

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License