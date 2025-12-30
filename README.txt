FastAPI Movie Backend

A production-ready FastAPI backend for a movie platform, featuring authentication, role-based access, favorites, audit logs, caching, background tasks.
This project is designed as a backend portfolio project, demonstrating clean architecture, modern Python tooling, and real-world backend patterns.

Features:
FastAPI with modular project structure
PostgreSQL + SQLAlchemy ORM
Alembic migrations
JWT Authentication
Role-based access control (Admin / User)
Favorites system (TMDB-based movies)
Audit logs for admin actions
Redis caching
Celery background tasks
Dependency overrides for testing
Pydantic schemas (input / output separation)

Project Structure
app/
├── api/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── movies.py
│   │   ├── favourites.py
│   │   ├── genres.py
│   │   └── audit.py
│
├── core/
│   ├── config.py
│   ├── security.py
│
├── db/
│   ├── base.py
│   ├── session.py
│   └── models/
│       ├── user.py
│       ├── movie.py
│       ├── genre.py
│       ├── favourite.py
│       └── audit.py
│
├── schemas/
│   ├── user.py
│   ├── movie.py
│   ├── genre.py
│   ├── favourite.py
│   └── audit.py
│
├── main.py
│
tests/
├── conftest.py
├── test_users.py
├── test_movies.py
├── test_genres.py
├── test_favourites.py
└── test_audit.py


Tech Stack
Python 3.10+
FastAPI
PostgreSQL
SQLAlchemy 2.0
Alembic
Redis
Celery
JWT (OAuth2 Password Flow)
Pytest


Environment Variables
Create a .env file:
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/movies_db
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_HOST=localhost
REDIS_PORT=6379

Database Setup
1️)Create database
CREATE DATABASE movies_db;

2)Run migrations
alembic upgrade head

3)Run the Application
uvicorn app.main:app --reload


API will be available at:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

Authentication
Uses JWT tokens
OAuth2 Password Flow
Access token required for protected endpoints
Role-based access:
USER
ADMIN

Example login:
POST /api/auth/login

Favorites System
Users can add movies to favorites
Check if a movie is already in favorites
Prevents duplicates
Stored in relational table (user_id + movie_id)

Audit Logs
Admin actions are logged

Tracks:
Admin user
Target user (optional)
Action description
Timestamp

Testing
Run all tests:
pytest


Testing includes:
Dependency overrides
Test database session
Authenticated user fixtures
CRUD endpoint coverage

Background Tasks (Celery)
Celery workers handle background jobs
Redis used as broker and cache

Designed for:
Logging
Notifications
Async data processing

