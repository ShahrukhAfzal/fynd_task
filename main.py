import jwt

from typing import List

from fastapi import Depends, FastAPI, HTTPException, status

from app import schemas
from app.models import Base
from app import crud

from app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
JWT_SECRET = 'my_secret_key'

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends(),
                   db: Session = Depends(get_db)):
    """
    use to access the api
    """
    user_obj = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    user_obj = user_obj.first()
    user_obj_dict = {
        'user_name': user_obj.email,
        'password': user_obj.password
    }
    token = jwt.encode(user_obj_dict, JWT_SECRET)

    return {'access_token': token, 'token_type': 'bearer'}


#  USER
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = crud.create_user(db=db, user=user)
    return created_user


@app.get("/users/", )
def read_users(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db),
               token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int,
              db: Session = Depends(get_db),
              token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# MOVIES
@app.get("/movies/")
def read_movies(skip: int = 0,
                limit: int = 100,
                search_by_name: str = None,
                db: Session = Depends(get_db)):
    movies = crud.get_movies(db, search_by_name, skip, limit)
    return movies


@app.get("/movies/{movie_id}")
def read_movies(movie_id: int,
                db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id)
    if movie:
        return movie
    return "No movie exists with this id."


@app.post("/movies/", response_model=schemas.MovieCreate)
def create_movies(movie: schemas.MovieCreate,
                  db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    new_movie = crud.create_movie(db, movie=movie)

    return new_movie


@app.post("/movies/{movie_id}")
def delete_movies(movie_id: int,
                  db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    is_deleted = crud.delete_movie(db, movie_id)
    if is_deleted:
        return "Deleted successfully"
    return "No such object exists"


@app.put("/movies/{movie_id}", response_model=schemas.MovieUpdate)
def update_movies(movie_id: int,
                  movie: schemas.MovieUpdate,
                  db: Session = Depends(get_db),
                  token: str = Depends(oauth2_scheme)):
    return crud.update_movie(db, movie_id, movie)

