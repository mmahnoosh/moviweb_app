from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    user_movies = db.relationship("UserMovies", back_populates="user", cascade="all, delete")
    movies = db.relationship("Movie", secondary="user_movies", backref="users", viewonly=True)

    def __repr__(self):
        return f"id: {self.id} name:{self.name}"

    def __str__(self):
        return f"name:{self.name}"


class Movie(db.Model):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    director = Column(String(100), nullable=True)
    release_year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)
    poster = Column(String, nullable=True)

    user_movies = db.relationship("UserMovies", back_populates="movie", cascade="all, delete")

    def __repr__(self):
        return (f"id: {self.id} title:{self.title} director:{self.director} "
                f"release_year:{self.release_year} rating:{self.rating}")

    def __str__(self):
        return (f"title:{self.title} director:{self.director} "
                f"release_year:{self.release_year} rating:{self.rating}")


class UserMovies(db.Model):
    __tablename__ = 'user_movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)
    movie_rating = Column(Float, nullable=True)

    user = db.relationship("User", back_populates="user_movies")
    movie = db.relationship("Movie", back_populates="user_movies")
