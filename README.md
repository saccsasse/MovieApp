FastAPI Movie Backend

This project is my main backend portfolio project and represents the full scope of my backend development knowledge. It is a production-oriented REST API built with modern Python technologies, designed with scalability, security, and maintainability in mind.
The application provides user authentication, role-based access control, movie-related endpoints, background processing, caching, database migrations, and full test coverage — all implemented from scratch.

Tech Stack:
- Python 3.10+
- FastAPI, TMDB external movie API
- PostgreSQL
- SQLAlchemy mapping 2.0
- Alembic migrations
- Json Web Token authentication
- OAuth2 Password Flow
- Role-based (Admin/User) authorization
- Redis cache
- Celery tasks background
- HTTPS protocols
- Pydantic shemas
- Async Support
- Pytest


Features:
- FastAPI with modular project structure
- PostgreSQL + SQLAlchemy ORM
- Alembic migrations
- Enum types & constraints
- JWT-based login & registration
- Routing protocols
- Asynchronious work
- Query Optimization
- Authentication System
- Role-based access control (Admin / User)
- Favorites system (TMDB-based movies)
- Audit logs for admin actions
- Redis caching
- Movies CRUD operations
- Genres support
- Dependency Injection
- Clear separation of concerns
- Modular routers
- Discover & filter endpoints
- Celery background tasks
- Dependency overrides for testing
- Pydantic schemas (input / output separation)


Environment Variables created in a .env file


Database Setup
1) Create virtual environment
   .venv\Scripts\activate

2) Install dependencies
   pip install -r requirements.txt

3) Environment variables
   Create .env based on .env.example and configure:
   Database
   JWT secrets
   Redis
   Celery

4) Run migrations
   alembic upgrade head

5) Create database
   CREATE DATABASE movies_db;

6) Run the Application
   uvicorn app.main:app --reload

API will be available at:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


What system can do:
  
User registration with secure password hashing (bcrypt)
User login with JWT access tokens
Role-based access control (USER, ADMIN)
Protected routes using dependency injection
Token validation and current-user resolution

Create and store users in PostgreSQL
Retrieve authenticated user profile
Activate / deactivate users
Enforce unique usernames and emails
Admin-only actions for user management
Audit logging for admin actions (if enabled)

Store movie data in a relational database
Retrieve movies by ID
Persist movie metadata (title, language, popularity, release date, ratings)
Prevent duplicate movie records
Optimized queries with indexing

Add movies to user favorites
Remove movies from favorites
Check if a movie is already in favorites
Prevent duplicate favorites (unique user_id + movie_id constraint)
Retrieve a list of all user favorites
Fully normalized relational table (users ↔ movies)

Discover popular or trending movies
Filter movies by parameters (e.g. popularity, language)
Pagination-ready endpoints
Cached responses using Redis (where applicable)

Retrieve a list of available movie genres
Expose genres via public API endpoint
Use genres for filtering and categorization
Genre schema optimized for frontend consumption

Background tasks handled with Celery
Async processing for heavy or delayed operations
Redis used as message broker / cache backend

PostgreSQL as the main relational database
SQLAlchemy ORM with clean model separation
Alembic migrations for schema versioning
Enum-based database roles (USER, ADMIN)
Strong constraints and indexes for data integrity

Modular project structure
Clear separation of concerns (routers, schemas, services, models)
Dependency Injection for database and auth
Environment-based configuration
Production-ready API design patterns

RESTful API design
JSON-based communication
Ready for frontend or mobile integration
Scalable architecture suitable for real-world applications

Audit Logs
