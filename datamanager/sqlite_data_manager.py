from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from data_model import User, Movie, UserMovies
from datamanager.data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, app):
        self.db = SQLAlchemy(app)

    def add_item(self, item):
        try:
            self.db.session.add(item)
            self.db.session.commit()
            return item
        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def get_all_users(self):
        try:
            return self.db.session.query(User).all()
        except SQLAlchemyError:
            print("Error fetching users")
            return []

    def get_all_movies(self):
        try:
            return self.db.session.query(Movie).all()
        except SQLAlchemyError:
            print("Error fetching movies")
            return []

    def get_user_movies(self, user_id):
        try:
            user = self.db.session.get(User, user_id)
            if not user:
                return None
            movies = user.movies

            return movies

        except SQLAlchemyError:
            print("Error fetching users and Movies")
            return []


    def get_user_by_name(self, username):
        try:
            existing_user = self.db.session.query(User).filter_by(name=username).first()
            if not existing_user:
                return "Error"
            return existing_user
        except SQLAlchemyError:
            return []

    def get_movie(self, movie_id):
        """Gets a movie by movie ID."""
        try:
            existing_movie = self.db.session.get(Movie, movie_id)
            if not existing_movie:
                return None
            return existing_movie
        except SQLAlchemyError:
            return []

    def add_user(self, username):
        try:
            existing_user = self.db.session.query(User).filter_by(name=username).first()
            if existing_user:
                return None
            user = User(name=username)
            return self.add_item(user)
        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def add_movie_to_user(self, movie_id, user_id):
        try:
            existing = self.db.session.query(UserMovies).filter_by(movie_id=movie_id,
                                                                   user_id=user_id).first()
            if existing:
                return existing
            new_entry = UserMovies(movie_id=movie_id, user_id=user_id)
            self.db.session.add(new_entry)
            self.db.session.commit()
            return new_entry

        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def add_movie(self, movie):
        try:
            existing_movie = self.db.session.query(Movie).filter_by(title=movie.title).first()
            if existing_movie:
                return None
            return self.add_item(movie)

        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def update_movie(self, movie_id, user_id, rating):
        if not rating or not isinstance(rating, (float, int)):
            return None
        try:
            movie = self.db.session.get(Movie, movie_id)
            if not movie:
                return None
            user_movie = self.db.session.query(UserMovies).filter_by(user_id=user_id,
                                                                     movie_id=movie_id).first()
            if not user_movie:
                return None
            user_movie.movie_rating = float(rating)
            self.db.session.commit()
            return movie

        except SQLAlchemyError:
            return None


    def delete_user_movie(self, movie_id, user_id):
        try:
            movie = self.db.session.get(Movie, movie_id)
            if not movie:
                return None
            user_movie = self.db.session.query(UserMovies).filter_by(user_id=user_id,
                                                                     movie_id=movie_id).first()
            if not user_movie:
                return None
            self.db.session.delete(user_movie)
            if not self.db.session.query(UserMovies).filter_by(movie_id=movie_id).first():
                self.db.session.delete(movie)
            self.db.session.commit()
            return movie
        except SQLAlchemyError:
            print("Database error while retrieving user movies")
            return []

    def delete_user(self, user_id):
        try:
            user = self.db.session.get(User, user_id)
            print(user.movies)
            if not user:
                return None
            movie_ids = [movie.id for movie in user.movies]
            print(movie_ids)
            self.db.session.delete(user)
            self.db.session.commit()
            for movie_id in movie_ids:
                other_links = self.db.session.query(UserMovies).filter_by(movie_id=movie_id).first()
                print(other_links)
                if not other_links:
                    self.db.session.query(Movie).filter_by(id=movie_id).delete()

            return user.name
        except SQLAlchemyError as error:
            self.db.session.rollback()
            print(f"Error fetching user:{error}")
            return []