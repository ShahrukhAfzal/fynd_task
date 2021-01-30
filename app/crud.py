from sqlalchemy.orm import Session

from app import schemas, models


# USER
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# MOVIES
def get_movies(db: Session, skip: int = 0, limit: int = 100):
    movies_data = db.query(models.Movie).offset(skip).limit(limit).all()
    for movie in movies_data:
        movie.genres

    return movies_data


def get_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        movie.genres

    return movie


def create_movie(db: Session, movie: schemas.MovieCreate):
    new_movie = models.Movie(name=movie.name,
        director=movie.director,
        imdb_score=movie.imdb_score)

    db.add(new_movie)
    genres = movie.genre
    db.commit()
    if genres:
        create_genre(db, genres, new_movie)

    db.refresh(new_movie)
    new_movie.genre = genres
    return new_movie


def create_genre(db, genres, new_movie):

    for genre_name in genres:
        genre = db.query(models.Genre).filter(
            models.Genre.name == genre_name).first()

        if not genre:
            genre = models.Genre(name=genre_name)
            db.add(genre)
            db.commit()

        genre.movies.append(new_movie)
        db.commit()

