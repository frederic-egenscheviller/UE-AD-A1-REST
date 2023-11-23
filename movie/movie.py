import json

import requests
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

# Configuration
PORT = 3200
HOST = '0.0.0.0'
OMBDAPI = 'http://www.omdbapi.com/'
API_KEY = '4e8a7dad'

# Load initial movies data from a JSON file
with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


@app.route("/", methods=['GET'])
def home():
    """
    Home route to welcome users.

    Returns:
        Response: HTML response with a welcome message.
    """
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/template", methods=['GET'])
def template():
    """
    Example route using an HTML template.

    Returns:
        Response: HTML response using a template.
    """
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


@app.route("/json", methods=['GET'])
def get_json():
    """
    Retrieve all movies in JSON format.

    Returns:
        Response: JSON response with the list of movies.
    """
    res = make_response(jsonify(movies), 200)
    return res


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    """
    Get details of a movie by its ID.

    Args:
        movieid (str): The ID of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "movie ID not found"}), 400)


@app.route("/moviesratingbetterthan/<rate>", methods=['GET'])
def get_movie_with_rating_better_than(rate):
    """
    Get movies with a rating better than a specified value.

    Args:
        rate (str): The minimum rating.

    Returns:
        Response: JSON response with the list of movies or an error message.
    """
    movies_json_list = []

    for movie in movies:
        # Check if the movie rating is better than the specified value
        if float(movie["rating"]) > float(rate):
            movies_json_list.append(movie)

    if movies_json_list:
        res = make_response(jsonify(movies_json_list), 200)
        return res
    return make_response(jsonify({"error": "movie with rate better than " + str(rate) + " not found"}), 400)


@app.route("/moviesbytitle/<movietitle>", methods=['GET'])
def get_movie_bytitle(movietitle):
    """
    Get details of a movie by its title.

    Args:
        movietitle (str): The title of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    for movie in movies:
        if str(movie["title"]) == str(movietitle):
            return make_response(jsonify(movie), 200)

    return make_response(jsonify({"error": "movie title not found"}), 400)


@app.route("/movies", methods=['POST'])
def create_movie():
    """
    Create a new movie.

    Returns:
        Response: JSON response with the new movie details or an error message.
    """
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(req["id"]):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify(req), 200)
    return res


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    """
    Update the rating of a movie by its ID.

    Args:
        movieid (str): The ID of the movie.
        rate (str): The new rating.

    Returns:
        Response: JSON response with the updated movie details or an error message.
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


@app.route("/movies/<movieid>", methods=['PUT'])
def update_movie(movieid):
    """
    Update the details of a movie by its ID.

    Args:
        movieid (str): The ID of the movie.

    Returns:
        Response: JSON response with the updated movie details or an error message.
    """
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["title"] = req["title"]
            movie["rating"] = req["rating"]
            movie["director"] = req["director"]
            return make_response(jsonify(movie), 200)

    movies.append(req)
    return make_response(jsonify(req), 200)


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    """
    Delete a movie by its ID.

    Args:
        movieid (str): The ID of the movie.

    Returns:
        Response: JSON response with the deleted movie details or an error message.
    """
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


@app.route("/movies-released/<title>", methods=['GET'])
def get_movie_released_date(title):
    """
    Get details of a movie by its title.

    Args:
        title (str): The title of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    params = {
        't': title,
        'apikey': API_KEY
    }

    response = requests.get(OMBDAPI, params=params)

    if response.status_code == 200:
        # Return only the released date of the movie using the OMDb API
        return make_response(jsonify(response.json().get("Released")), 200)
    else:
        make_response(jsonify({"error": "movie title not found"}), 400)


@app.route("/moviesbytitle/<movietitle>/detailed", methods=['GET'])
def get_movie_detailed(movietitle):
    """
    Get details of a movie by its title.

    Args:
        title (str): The title of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    params = {
        't': movietitle,
        'apikey': API_KEY
    }

    response = requests.get(OMBDAPI, params=params)

    if response.status_code == 200:
        # Return all the details of the movie using the OMDb API
        return make_response(jsonify(response.json()), 200)
    else:
        make_response(jsonify({"error": "movie title not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
