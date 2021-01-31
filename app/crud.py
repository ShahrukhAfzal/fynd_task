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
def get_movies(db: Session,
               search_by_name: str = None,
               skip: int = 0,
               limit: int = 100):

    if search_by_name:
        search = f"%{search_by_name}%"
        movies_data = db.query(models.Movie).filter(models.Movie.name.like(search)).offset(skip).limit(limit).all()
    else:
        movies_data = db.query(models.Movie).offset(skip).limit(limit).all()

    for movie in movies_data:
        movie.genres

    return movies_data


def get_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        movie.genres
        return movie

    return None


def delete_movie(db: Session, movie_id: int):
    obj = db.query(models.Movie).filter(models.Movie.id == movie_id)
    first_obj = obj.first()
    if first_obj:
        first_obj.genres.clear()
        db.add(first_obj)
        db.commit()

        obj.delete()
        db.commit()

        return True
    return False


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


def update_movie(db: Session, movie_id: int, update_movie: schemas.MovieUpdate):
    obj = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
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
        genre = db.query(models.Genre).filter(
            models.Genre.name == genre_name).first()

        if not genre:
            genre = models.Genre(name=genre_name)
            db.add(genre)
            db.commit()

        genre.movies.append(new_movie)
        db.commit()


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(
        models.User.email==username,
        models.User.password==password
    )
    if user.first():
        return user

    return False
