🚀 TodoBackend API - FastAPI Backend
A robust, production-ready Todo application backend built with FastAPI, featuring JWT authentication, rate limiting, and PostgreSQL integration.

🛠 Tech Stack
Framework: FastAPI + Python 3.11+

Database: PostgreSQL with SQLAlchemy ORM

Authentication: JWT Tokens with HTTPBearer

Security: Password hashing with bcrypt

Rate Limiting: SlowAPI for request throttling

Validation: Pydantic v2

Logging: Custom configurable logging system

🚀 Quick Start
Prerequisites
Python 3.11+

PostgreSQL

pip

Installation
bash
# Clone repository
git clone https://github.com/YourFavoriteBackendGirl/todo-backend-api.git
cd todo-backend-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
Environment Variables
env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
Run the Application
bash
# Start the server
uvicorn main:app --reload

# Access API docs at: http://localhost:8000/docs
📚 API Documentation
Once running, access:

Swagger UI: /docs - Interactive API documentation

ReDoc: /redoc - Alternative documentation

🔐 Authentication
Register User
http
POST /auth/
Content-Type: application/json

{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123"
}
Login
http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
Response:

json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
Protected Endpoints
Include the token in headers:

http
Authorization: Bearer your_jwt_token_here
📝 API Endpoints
Authentication
Method	Endpoint	Description	Auth Required
POST	/auth/	Register new user	❌
POST	/auth/login	Login user	❌
POST	/auth/token	OAuth2 compatible login	❌
Users
Method	Endpoint	Description	Auth Required
GET	/users/me	Get current user	✅
PUT	/users/change-password	Change password	✅
Todos
Method	Endpoint	Description	Auth Required
GET	/todos/	Get all user todos	✅
POST	/todos/	Create new todo	✅
GET	/todos/{id}	Get specific todo	✅
PUT	/todos/{id}	Update todo	✅
PUT	/todos/{id}/complete	Mark todo complete	✅
DELETE	/todos/{id}	Delete todo	✅
🗄 Database Models
User
python
id: UUID (Primary Key)
email: String (Unique)
first_name: String
last_name: String
password_hash: String
Todo
python
id: UUID (Primary Key)
user_id: UUID (Foreign Key)
description: String
due_date: DateTime (Optional)
is_completed: Boolean
created_at: DateTime
completed_at: DateTime (Optional)
priority: Enum (Normal, Low, Medium, High, Top)
🛡 Security Features
✅ JWT Authentication with bearer tokens

✅ Password Hashing using bcrypt with SHA256 fallback

✅ Rate Limiting (5 requests/minute for auth endpoints)

✅ SQL Injection Protection via SQLAlchemy

✅ CORS Enabled for frontend integration

✅ Input Validation with Pydantic models

🧪 Testing the API
Using FastAPI Docs
Visit http://localhost:8000/docs

Register a new user via /auth/ endpoint

Login via /auth/login to get JWT token

Click "Authorize" button and enter: Bearer your_token_here

Test protected endpoints

Using curl
bash
# Register
curl -X POST "http://localhost:8000/auth/" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","first_name":"Test","last_name":"User","password":"password123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get todos (with token)
curl -X GET "http://localhost:8000/todos/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
🔧 Development
Project Structure
text
src/
├── auth/
│   ├── controller.py    # Auth routes
│   ├── service.py       # Business logic
│   └── schemas.py       # Pydantic models
├── entities/
│   ├── user.py          # User model
│   └── todo.py          # Todo model
├── todos/
│   ├── controller.py    # Todo routes
│   ├── service.py       # Todo logic
│   └── schemas.py       # Todo schemas
├── users/
│   ├── controller.py    # User routes
│   ├── service.py       # User logic
│   └── schemas.py       # User schemas
├── database/
│   └── core.py          # DB configuration
└── main.py              # App entry point
Running Tests
bash
# Add tests and run (when implemented)
pytest tests/
🚀 Deployment
Production Ready Features
✅ Database connection pooling

✅ Environment-based configuration

✅ Comprehensive error handling

✅ Structured logging

✅ Rate limiting

✅ Input validation

Deploy to Production
Set SECRET_KEY environment variable

Configure production PostgreSQL database

Set up reverse proxy (Nginx)

Use process manager (PM2/Supervisor)

Enable HTTPS

🤝 Contributing
This project is perfect for frontend developers looking to:

Practice integrating with a real backend API

Learn JWT authentication flows

Build full-stack applications

Improve backend understanding

Frontend developers: Clone this and build your dream todo app frontend!

📄 License
MIT License - feel free to use this project for learning and development.

👩‍💻 Author
YourFavoriteBackendGirl - Building robust backends with ❤️

🐛 Issues & Support
Found a bug? Want to contribute? Open an issue or PR on GitHub!