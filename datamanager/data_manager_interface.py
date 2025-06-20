from abc import ABC, abstractmethod
from typing import List, Optional, Union

from data_model import User, Movie, UserMovies


class DataManagerInterface(ABC):
    """Abstract base class defining the interface for data managers."""

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Returns a list of all users."""
        pass

    @abstractmethod
    def get_all_movies(self) -> List[Movie]:
        """Returns a list of all movies."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id: int) -> Optional[List[UserMovies]]:
        """
        Retrieves all movies associated with a given user.

        :param user_id: ID of the user
        :return: List of UserMovies or None if user not found
        """
        pass

    @abstractmethod
    def get_user_movie(self, user_id: int, movie_id: int) -> Optional[UserMovies]:
        """
        Retrieves a specific UserMovies entry for a given user and movie.

        :param user_id: ID of the user
        :param movie_id: ID of the movie
        :return: UserMovies entry or None if not found
        """
        pass

    @abstractmethod
    def get_user_by_name(self, username: str) -> Union[User, str, None]:
        """
        Retrieves a user by name.

        :param username: Name of the user
        :return: User object, "Error" or None
        """
        pass

    @abstractmethod
    def get_movie(self, movie_id: int) -> Optional[Movie]:
        """
        Retrieves a movie by its ID.

        :param movie_id: ID of the movie
        :return: Movie object or None if not found
        """
        pass

    @abstractmethod
    def add_item(self, item: Union[User, Movie, UserMovies]) -> Optional[
        Union[User, Movie, UserMovies]]:
        """
        Generic method to add an item to the database.

        :param item: SQLAlchemy model instance
        :return: The added item or None on failure
        """
        pass

    @abstractmethod
    def add_user(self, username: str) -> Optional[User]:
        """
        Adds a new user.

        :param username: Name of the user
        :return: User object or None if user already exists or error occurs
        """
        pass

    @abstractmethod
    def add_movie(self, movie: dict, user_id: int) -> Optional[str]:
        """
        Adds a movie and links it to a user.

        :param movie: Dictionary containing movie data
        :param user_id: ID of the user
        :return: Error message or None on success
        """
        pass

    @abstractmethod
    def add_movie_to_user(self, movie: Movie, user_id: int) -> Optional[str]:
        """
        Links an existing movie to a user.

        :param movie: Movie object
        :param user_id: ID of the user
        :return: Error message or None on success
        """
        pass

    @abstractmethod
    def update_movie(self, movie: UserMovies, rating: float) -> Optional[UserMovies]:
        """
        Updates the user-specific movie rating.

        :param movie: UserMovies entry
        :param rating: New rating
        :return: Updated UserMovies entry or None on failure
        """
        pass

    @abstractmethod
    def delete_movie(self, user_id: int, movie_id: int) -> Optional[Movie]:
        """
        Deletes a movie from a user's collection and possibly from the database.

        :param user_id: ID of the user
        :param movie_id: ID of the movie
        :return: The deleted Movie or None
        """
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> Optional[None]:
        """
        Deletes a user and their associated movies.

        :param user_id: ID of the user
        :return: None
        """
        pass
