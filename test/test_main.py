import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200


def test_create_user():
    response = client.post('/users/',
                            json={
                                    "email": "test_user" + uuid.uuid4().hex[:8],
                                    "name": "string",
                                    "password": "123456"
                                }
                            )
    assert response.status_code == 200


def test_get_user_without_auth():
    response = client.get('/users/')

    assert response.status_code == 401


def test_get_movies():
    response = client.get('/movies')
    assert response.status_code == 200


def test_create_movies_without_auth():
    response = client.post('/movies/',
        json={
            "popularity": 83.0,
            "director": "Victor Fleming",
            "genre": [
              "Adventure",
              " Family",
              " Fantasy",
              " Musical"
            ],
            "imdb_score": 8.3,
            "name": "The Wizard of Oz"
        })

    assert response.status_code == 401


def test_create_movies_with_auth():
    response = client.post('/movies/',
        json={
            "popularity": 83.0,
            "director": "Victor Fleming",
            "genre": [
              "Adventure",
              " Family",
              " Fantasy",
              " Musical"
            ],
            "imdb_score": 8.3,
            "name": "The Wizard of Oz"
        })

    assert response.status_code == 401
