from sqlalchemy import (Boolean, Column, ForeignKey,
                        Integer, String, Float, Table)

from app.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


# MOVIES
MOVIE_GENRE = Table('movie_genre',
                    Base.metadata,
                    Column('movies_id', Integer, ForeignKey('movies.id')),
                    Column('genres_id', Integer, ForeignKey('genres.id'))
                    )

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    director = Column(String)
    imdb_score = Column(Float)
    popularity = Column(String)
    genres = relationship('Genre', secondary=MOVIE_GENRE, backref='movies')


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
