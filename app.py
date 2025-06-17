import os

from flask import Flask, render_template, request, abort

from data_model import Movie
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'moviwebapp.db')}"

data_manager = SQLiteDataManager(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Displays all movies associated with a specific user."""
    movies = data_manager.get_user_movies(user_id)

    return render_template('user_movies.html', movies=movies, user_id=user_id)


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('list_users.html', users=users)


@app.route('/movies')
def list_movies():
    movies = data_manager.get_all_movies()
    return render_template('list_movies.html', movies=movies, active_page='movies')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Route to add a new user."""
    if request.method == 'POST':
        username = request.form.get('name')
        if not username:
            return render_template('add_user.html', error='Username is required')

        result = data_manager.add_user(username)
        if not result:
            return render_template('add_user.html', error='Failed to add user (maybe duplicate?)')

        return render_template('add_user.html', message=f'User added successfully')

    return render_template('add_user.html')


@app.route('/users/add_movie', methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        rating = request.form.get('rating', '').strip()
        poster = request.form.get('poster', '').strip()

        if all([title, director, year]):
            try:
                release_year = int(year)

                if not rating:
                    rating = 0.0
                else:
                    rating = float(rating.replace(",", "."))

                new_movie = Movie(
                    name=title,
                    director=director,
                    release_year=release_year,
                    rating=rating,
                    poster=poster
                )

                result = data_manager.add_movie(new_movie)
                if not result:
                    return render_template('error.html', error="Movie already exists.")

                return render_template('add_movie.html', message="Movie added successfully.")

            except (ValueError, TypeError):
                return render_template('error.html', error="Invalid year or rating format.")

        return render_template('error.html', error="Missing required movie data.")

    return render_template('add_movie.html')


@app.route('/users/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(movie_id):
    movie = data_manager.get_movie(movie_id)
    if not movie:
        abort(400, description="Movie not found")

    if request.method == 'POST':
        rating = request.form.get('rating')
        if not rating:
            return render_template('update_movie.html', movie=movie)
        rating_str = rating.replace(',', '.')

        try:
            rating_float = float(rating_str)
            if not 0.0 < rating_float < 10.0:
                return render_template('update_movie.html', movie=movie,
                                       error="Rating must be between 0 and 10")
        except (ValueError, TypeError):
            return render_template('update_movie.html', movie=movie,
                                   error="Please enter a valid rating between 0 and 10.")

        result = data_manager.update_movie(movie, rating_float)
        if not result:
            if not result:
                return render_template("update_movie.html", movie=movie,
                                       error="No update was made")

    return render_template('update_movie.html', movie=movie)


@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", error=error)


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
