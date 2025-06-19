import os

import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError, Timeout

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie_data(title):
    fetch_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    try:
        response = requests.get(fetch_url, headers=headers)
        response.raise_for_status()
    except(HTTPError, ConnectionError, Timeout) as error:
        print(f"Request error occurred: {error}")
        return None

    try:
        movie = response.json()
    except ValueError as error:
        print(f"Error parsing JSON: {error}")
        return None

    return {
        'Title': movie.get('Title'),
        'Director': movie.get('Director'),
        'Year': movie.get('Year'),
        'imdbRating': movie.get('imdbRating'),
        'Poster': movie.get('Poster')
    }


def check_poster_availability(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return url
    except(ConnectionError, Timeout, HTTPError):
        return "/static/fallback_poster.jpeg"
