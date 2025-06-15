from flask import Flask
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
data_manager = SQLiteDataManager('moviwebapp.db')  # Use the appropriate path to your Database


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string

@app.route('/users/<user_id>')
def user_movies():
    pass

@app.route('/add_user')
def add_user():
    pass


@app.route('/users/<user_id>/add_movie')
def add_movie():
    pass

@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie():
    pass

@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie():
    pass
if __name__ == '__main__':
    app.run(debug=True)