from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

from data_model import User, Movie, UserMovies
from datamanager.data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, app):
        self.db = SQLAlchemy(app)

    def get_all_users(self):
        """Returns a list of all users."""
        try:
            return self.db.session.query(User).all()
        except SQLAlchemyError:
            print("Error fetching users")
            return []

    def get_all_movies(self):
        """Returns a list of all movies."""
        try:
            return self.db.session.query(Movie).all()
        except SQLAlchemyError:
            print("Error fetching movies")
            return []

    def get_user_movies(self, user_id):
        """
            Retrieves all movies associated with a given user.

            :param user_id: ID of the user
            :return: List of UserMovies or None if user not found
        """
        try:
            user = self.db.session.get(User, user_id)
            if not user:
                return None
            movies = user.user_movies

            return movies

        except SQLAlchemyError:
            print("Error fetching users and Movies")
            return []

    def get_user_movie(self, user_id, movie_id):
        """
            Retrieves a specific UserMovies entry for a given user and movie.

            :param user_id: ID of the user
            :param movie_id: ID of the movie
            :return: UserMovies entry or None if not found
        """
        try:
            existing_movie = self.db.session.query(UserMovies).filter_by(user_id=user_id,
                                                                         movie_id=movie_id).first()
            if not existing_movie:
                return None
            return existing_movie
        except SQLAlchemyError:
            return []

    def get_user_by_name(self, username):
        """
            Retrieves a user by name.

            :param username: Name of the user
            :return: User object, "Error" or None
        """
        try:
            existing_user = self.db.session.query(User).filter_by(name=username).first()
            if not existing_user:
                return "Error"
            return existing_user
        except SQLAlchemyError:
            return []

    def get_movie(self, movie_id):
        """
            Retrieves a movie by its ID.

            :param movie_id: ID of the movie
            :return: Movie object or None if not found
        """
        try:
            existing_movie = self.db.session.get(Movie, movie_id)
            if not existing_movie:
                return None
            return existing_movie
        except SQLAlchemyError:
            return []

    def add_item(self, item):
        """
            Generic method to add an item to the database.

            :param item: SQLAlchemy model instance
            :return: The added item or None on failure
        """
        try:
            self.db.session.add(item)
            self.db.session.commit()
            self.db.session.refresh(item)
            return item
        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def add_user(self, username):
        """
            Adds a new user.

            :param username: Name of the user
            :return: User object or None if user already exists or error occurs
        """
        try:
            existing_user = self.db.session.query(User).filter_by(name=username).first()
            if existing_user:
                return None
            user = User(name=username)
            return self.add_item(user)
        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def add_movie_to_user(self, movie, user_id):
        """
            Links an existing movie to a user.

            :param movie: Movie object
            :param user_id: ID of the user
            :return: Error message or None on success
        """
        try:
            existing = self.db.session.query(UserMovies).filter_by(movie_id=movie.id,
                                                                   user_id=user_id).first()
            if existing:
                return "Movie already exists"

            new_entry = UserMovies(movie_id=movie.id, user_id=user_id, movie_rating=movie.rating)

            self.db.session.add(new_entry)
            self.db.session.commit()
            return None

        except SQLAlchemyError:
            self.db.session.rollback()
            return "Error with the database"

    def add_movie(self, movie, user_id):
        """
            Adds a movie and links it to a user.

            :param movie: Dictionary containing movie data
            :param user_id: ID of the user
            :return: Error message or None on success
        """
        try:
            existing_movie = self.db.session.query(Movie).filter_by(
                title=movie.get("Title")).first()
            if existing_movie:
                return self.add_movie_to_user(existing_movie, user_id)
            new_movie = Movie(
                title=movie.get('Title'),
                director=movie.get('Director'),
                release_year=movie.get('Year'),
                rating=movie.get('imdbRating'),
                poster=movie.get('Poster')

            )
            new_movie = self.add_item(new_movie)
            if not new_movie:
                return "Error with the database"
            return self.add_movie_to_user(new_movie, user_id)

        except SQLAlchemyError:
            self.db.session.rollback()
            return None

    def update_movie(self, movie, rating):
        """
            Updates the user-specific movie rating.

            :param movie: UserMovies entry
            :param rating: New rating
            :return: Updated UserMovies entry or None on failure
        """
        if not rating or not isinstance(rating, (float, int)) or not movie:
            return None
        try:
            movie.movie_rating = float(rating)
            self.db.session.commit()
            self.db.session.refresh(movie)
            return movie

        except SQLAlchemyError:
            return None

    def delete_movie(self, user_id, movie_id):
        """
            Deletes a movie from a user's collection and possibly from the database.

            :param user_id: ID of the user
            :param movie_id: ID of the movie
            :return: The deleted Movie or None
        """
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
        """
            Deletes a user and their associated movies.

            :param user_id: ID of the user
            :return: None
        """
        try:
            user_movies = self.db.session.query(UserMovies).filter_by(user_id=user_id).all()
            movie_ids = [movie.id for movie in user_movies]
            self.db.session.query(UserMovies).filter_by(user_id=user_id).delete()
            self.db.session.query(User).filter_by(id=user_id).delete()
            self.db.session.commit()
            for movie_id in movie_ids:
                still_linked = self.db.session.query(UserMovies).filter_by(
                    movie_id=movie_id).first()
                if not still_linked:
                    self.db.session.query(Movie).filter_by(id=movie_id).delete()
            self.db.session.commit()
            return
        except SQLAlchemyError as error:
            self.db.session.rollback()
            print(f"Error fetching user:{error}")
            return []
