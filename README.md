# Todo API - FastAPI Backend   

A robust, high-performance RESTful API for a Todo application, built with FastAPI and PostgreSQL. This API provides a complete backend solution with full CRUD operations, user authentication, and secure data handling, ready for a frontend client to build upon.   

## 🚀 Features

· Full CRUD Operations: Create, Read, Update, and Delete todos with ease  
· User Authentication & Authorization: JWT-based secure authentication system  
· PostgreSQL Database: Reliable and scalable data persistence  
· FastAPI Performance: Lightning-fast responses with automatic interactive documentation  
· Pydantic Validation: Strong data typing and validation  
· CORS Enabled: Ready for frontend integration   
· Environment Configuration: Secure management of sensitive data  
· Modern Python: Built with Python 3.7+ features and async capabilities  


## 🛠 Tech Stack   

· Framework: FastAPI   
· Database: PostgreSQL  
· ORM: SQLAlchemy   
· Authentication: JWT (JSON Web Tokens)   
· Password Hashing: BCrypt   
· Deployment: Ready for deployment (Render, Heroku, etc.)   

## 📚 API Endpoints

Method |   Endpoint         |  Description Authentication  
-------|--------------------|---------------------------------
POST   |  api/auth/register |  User registration No    
POST   |  api/auth/login    |  User login No    
GET    |  api/todos         |  Get all user's todos Yes    
POST   |  api/todos         |  Create a new todo Yes    
GET    |  api/todos/{id}    |  Get a specific todo Yes    
PUT    |  api/todos/{id}    |  Update a todo Yes    
DELETE |  api/todos/{id}    |  Delete a todo Yes    


## 🔧 Installation & Setup    

1. Clone the repository    
   ```bash
   git clone https://github.com/Dabeey/todo-app-end-to-end-project.git
   cd todo-app-end-to-end-project
   ```
2. Create a virtual environment    
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies    
   ```bash
   pip install -r requirements.txt
   ```
4. Environment Configuration    
   Create a .env file with:
   ```
   DATABASE_URL=your_postgresql_connection_string
   SECRET_KEY=your_jwt_secret_key
   ALGORITHM=HS256
   ```
5. Run the application    
   ```bash
   uvicorn main:app --reload
   ```
6. Access API Documentation
   Visit http://localhost:8000/docs for interactive Swagger documentation.

## 🎯 Frontend Integration Ready    

This API is perfectly structured for frontend integration. Key features for frontend developers:    

· Clear, Consistent Endpoints: RESTful design patterns    
· Comprehensive Error Handling: Detailed error messages and status codes    
· JWT Authentication: Standard token-based auth flow    
· CORS Configured: Already set up for cross-origin requests    
· Interactive Documentation: Test endpoints directly at /docs    

## 🚀 Deployment      

Test endpoints using the interactive docs or tools like Postman.    

## 🤝 Contributing    

Frontend developers interested in building a React, Vue, Angular, or any JavaScript frontend for this API are welcome to contribute! The API is stable, well-documented, and ready for integration.    

## 📄 License    

This project is licensed under the MIT License.    
