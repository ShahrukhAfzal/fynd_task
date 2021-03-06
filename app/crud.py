from sqlalchemy.orm import Session

from app.schemas import (UserCreate, MovieCreate, MovieUpdate)
from app.models import (Movie, User, Genre)


# USER
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# MOVIES
def get_movies(db: Session,
               search_by_name: str = None,
               skip: int = 0,
               limit: int = 100):
    if search_by_name:
        search = f"%{search_by_name}%"
        movies_data = db.query(Movie).filter(Movie.name.like(search)).offset(skip).limit(limit).all()
    else:
        movies_data = db.query(Movie).offset(skip).limit(limit).all()

    for movie in movies_data:
        movie.genres

    return movies_data


def get_movie(db: Session, movie_id: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie:
        movie.genres
        return movie

    return None


def delete_movie(db: Session, movie_id: int):
    obj = db.query(Movie).filter(Movie.id == movie_id)
    first_obj = obj.first()
    if first_obj:
        first_obj.genres.clear()
        db.add(first_obj)
        db.commit()

        obj.delete()
        db.commit()

        return True
    return False


def create_movie(db: Session, movie: MovieCreate):
    new_movie = Movie(name=movie.name,
                      director=movie.director,
                      imdb_score=movie.imdb_score,
                      popularity=movie.popularity)

    db.add(new_movie)
    genres = movie.genre
    db.commit()
    if genres:
        create_genre(db, genres, new_movie)

    db.refresh(new_movie)
    new_movie.genre = genres
    return new_movie


def update_movie(db: Session, movie_id: int,
                 update_movie: MovieUpdate):
    obj = db.query(Movie).filter(Movie.id == movie_id).first()
    if obj:
        new_name = update_movie.name
        new_director = update_movie.director
        new_imdb_score = update_movie.imdb_score
        new_genre = update_movie.genre

        if new_name:
            obj.name = new_name
        if new_director:
            obj.director = new_director
        if new_imdb_score:
            obj.imdb_score = new_imdb_score

        db.add(obj)
        db.commit()

        return update_movie

    return None


def create_genre(db, genres, new_movie):
    for genre_name in genres:
        genre = db.query(Genre).filter(
            Genre.name == genre_name).first()

        if not genre:
            genre = Genre(name=genre_name)
            db.add(genre)
            db.commit()

        genre.movies.append(new_movie)
        db.commit()


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(
        User.email == username,
        User.password == password
    )
    if user.first():
        return user

    return False
