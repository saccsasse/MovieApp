import pytest

from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from datetime import date

from main import app

from app.db.session import Base, get_db
from app.db.models.user import User
from app.db.models.movie import Movie
from app.db.models.favourite import Favourite
from app.db.models.audit import AuditLog

from app.core.security import bcrypt_context
from app.core.enums import UserRole


TEST_DATABASE_URL = "postgresql://postgres:mypassword123@localhost/MovieApplicationDatabase_test"

engine = create_engine(
    TEST_DATABASE_URL,
    poolclass= StaticPool, #ensures all tests share the same DB connection
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def override_get_current_user():
    return {'username': 'admin', 'id': 1, 'user_role': 'admin'}
client = TestClient(app)


@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    user = User(
        username="admin",
        email="admin@example.com",
        first_name="Aliaksei",
        last_name="Ramanouski",
        hashed_password=bcrypt_context.hash("myadminpassword123"),
        role=UserRole.ADMIN,
        is_active=True
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_movie():
    movie = Movie(
        original_language="en",
        original_title="Test Movie",
        overview="Test overview",
        popularity=10.0,
        poster_path=None,
        release_date=date.today(),
        title="Test Movie",
        video=False,
        vote_average=8.0,
        vote_count=100
    )

    db = TestingSessionLocal()
    db.add(movie)
    db.commit()

    yield movie
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM movie;"))
        connection.commit()


@pytest.fixture
def test_favourite(test_user, test_movie):
    favourite = Favourite(
        user_id=test_user.id,
        movie_id=test_movie.id
    )

    db = TestingSessionLocal()
    db.add(favourite)
    db.commit()

    yield favourite
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM favourites;"))
        connection.commit()
