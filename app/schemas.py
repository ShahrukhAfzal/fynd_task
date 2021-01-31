from typing import List, Optional

from pydantic import BaseModel, validator


# USER SCHEMAS
class UserBase(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


# GENRE SCHEMAS
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True


# MOVIE SCHEMAS
class MovieBase(BaseModel):
    name: str
    director: str
    imdb_score: float
    popularity: float

    class Config:
        orm_mode = True


class MovieCreate(MovieBase):
    genre: List[str] = []


class MovieUpdate(BaseModel):
    name: Optional[str] = None
    director: Optional[str] = None
    imdb_score: Optional[float] = None
    genre: List[str] = []


class Movie(MovieBase):
    genre: Genre
    id: int
