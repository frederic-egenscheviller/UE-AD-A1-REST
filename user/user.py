import json
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

MOVIE_SERVICE_URL = "http://movie:3200"
BOOKING_SERVICE_URL = "http://booking:3201"

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    """
    Returns a welcome message for the User service.

    Returns:
        str: Welcome message in HTML format.
    """
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/user/<userid>", methods=['GET'])
def get_user_byid(userid):
    """
    Retrieves user information by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing user information or an error message.
    """
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "user ID not found"}), 400)


@app.route("/user", methods=['POST'])
def create_user():
    """
    Creates a new user based on the JSON request.

    Returns:
        Response: JSON response containing the new user information or an error message.
    """
    req = request.get_json()

    if all(key in req for key in ["id", "name", "last_active"]):
        if req["id"] not in [user["id"] for user in users]:
            users.append(req)
            return make_response(jsonify(req), 200)
        else:
            return make_response(jsonify({"error": "user already exists"}), 400)

    return make_response(jsonify({"error": "invalid user object format"}), 400)


@app.route("/user/<userid>", methods=['PUT'])
def update_user(userid):
    """
    Updates user information by user ID based on the JSON request.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing the updated user information or an error message.
    """
    req = request.get_json()

    if all(key in req for key in ["id", "name", "last_active"]):
        for user in users:
            if str(user["id"]) == str(userid):
                user["name"] = req["name"]
                user["last_active"] = req["last_active"]
                return make_response(jsonify(req), 200)
        users.append(req)
    return make_response(jsonify({"error": "invalid user object format"}), 400)


@app.route("/user/<userid>", methods=['DELETE'])
def delete_user(userid):
    """
    Deletes a user by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing the deleted user information or an error message.
    """
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "user ID not found"}), 400)


@app.route("/user-bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    """
    Retrieves user bookings from the Booking service by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing user bookings or an error message.
    """
    booking_response = requests.get(f"{BOOKING_SERVICE_URL}/bookings/{userid}")

    if booking_response.status_code == 200:
        user_bookings = booking_response.json()
        return make_response(jsonify(user_bookings), 200)
    else:
        return make_response(jsonify({"error": "user ID not found in Booking service"}), 400)


@app.route("/user-bookings/<userid>/detailed", methods=['GET'])
def get_detailed_userbookings(userid):
    """
    Retrieves detailed user bookings with movie information from the Booking and Movie services by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing detailed user bookings or an error message.
    """
    booking_response = requests.get(f"{BOOKING_SERVICE_URL}/bookings/{userid}")

    if booking_response.status_code == 200:
        user_bookings = booking_response.json()
        movie_infos = []
        for booking in user_bookings['dates']:
            for movie in booking['movies']:
                movie_response = requests.get(f"{MOVIE_SERVICE_URL}/movies/{movie}")
                movie_infos.append(movie_response.json())

        movie_info_map = {movie['id']: movie for movie in movie_infos}
        for date_info in user_bookings['dates']:
            for i, movie_id in enumerate(date_info['movies']):
                date_info['movies'][i] = movie_info_map.get(movie_id, {})

        return make_response(jsonify(user_bookings), 200)
    else:
        return make_response(jsonify({"error": "user ID not found in Booking service"}), 400)


@app.route("/bookings", methods=['GET'])
def get_booking_json():
    """
    Retrieves all bookings in JSON format.

    Returns:
        Response: JSON response containing all bookings.
    """
    response = requests.get(f"{BOOKING_SERVICE_URL}/bookings")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    """
    Retrieves booking information for a specific user by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing booking information or an error message.
    """
    response = requests.get(f"{BOOKING_SERVICE_URL}/bookings/{userid}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/bookings", methods=['POST'])
def create_booking():
    """
    Adds a new booking based on the JSON request.

    Returns:
        Response: JSON response containing the new booking information or an error message.
    """
    response = requests.post(f"{BOOKING_SERVICE_URL}/bookings", json=request.get_json())
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/bookings/<userid>", methods=['PUT'])
def update_booking_byuser(userid):
    """
    Updates booking information for a specific user by user ID based on the JSON request.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing the updated booking information or an error message.
    """
    response = requests.put(f"{BOOKING_SERVICE_URL}/bookings", json=request.get_json())
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/bookings/<userid>", methods=['DELETE'])
def delete_booking_byuser(userid):
    """
    Deletes a booking for a specific user by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing the deleted booking information or an error message.
    """
    response = requests.delete(f"{BOOKING_SERVICE_URL}/bookings/{userid}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/movies", methods=['GET'])
def get_movies_json():
    """
    Retrieve all movies in JSON format.

    Returns:
        Response: JSON response with the list of movies.
    """
    response = requests.get(f"{MOVIE_SERVICE_URL}/json")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    """
    Get details of a movie by its ID.

    Args:
        movieid (str): The ID of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    response = requests.get(f"{MOVIE_SERVICE_URL}/movies/{movieid}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/moviesratingbetterthan/<rate>", methods=['GET'])
def get_movie_with_rating_better_than(rate):
    """
    Get movies with a rating better than a specified value.

    Args:
        rate (str): The minimum rating.

    Returns:
        Response: JSON response with the list of movies or an error message.
    """
    response = requests.get(f"{MOVIE_SERVICE_URL}/moviesratingbetterthan/{rate}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/moviesbytitle/<movietitle>", methods=['GET'])
def get_movie_bytitle(movietitle):
    """
    Get details of a movie by its title.

    Args:
        movietitle (str): The title of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    response = requests.get(f"{MOVIE_SERVICE_URL}/moviesbytitle/{movietitle}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/movies", methods=['POST'])
def create_movie():
    """
    Create a new movie.

    Returns:
        Response: JSON response with the new movie details or an error message.
    """
    response = requests.post(f"{MOVIE_SERVICE_URL}/movies", json=request.get_json())
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/movies/<movieid>", methods=['PUT'])
def update_movie(movieid):
    """
    Update the details of a movie by its ID.

    Args:
        movieid (str): The ID of the movie.

    Returns:
        Response: JSON response with the updated movie details or an error message.
    """
    response = requests.put(f"{MOVIE_SERVICE_URL}/movies/{movieid}", json=request.get_json())
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    """
    Delete a movie by its ID.

    Args:
        movieid (str): The ID of the movie.

    Returns:
        Response: JSON response with the deleted movie details or an error message.
    """
    response = requests.delete(f"{MOVIE_SERVICE_URL}/movies/{movieid}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/movies-released/<title>", methods=['GET'])
def get_movie_released_date(title):
    """
    Get details of a movie by its title.

    Args:
        title (str): The title of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    response = requests.get(f"{MOVIE_SERVICE_URL}/movies-released/{title}")
    return make_response(jsonify(response.json()), response.status_code)


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
    response = requests.put(f"{MOVIE_SERVICE_URL}/movies/{movieid}/{rate}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/moviesbytitle/<movietitle>/detailed", methods=['GET'])
def get_movie_detailed(movietitle):
    """
    Get details of a movie by its title.

    Args:
        movietitle (str): The title of the movie.

    Returns:
        Response: JSON response with movie details or an error message.
    """
    response = requests.get(f"{MOVIE_SERVICE_URL}/moviesbytitle/{movietitle}/detailed")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/showtimes", methods=['GET'])
def get_showtimes():
    """
    Retrieve all showtimes.

    Returns:
        Response: JSON response containing the schedule.
    """
    response = requests.get(f"{BOOKING_SERVICE_URL}/showtimes")
    return make_response(jsonify(response.json()), 200)


@app.route("/showtimes", methods=['POST'])
def create_showtime():
    """
    Create a new showtime.

    Returns:
        Response: JSON response with the new showtime or an error message.
    """
    response = requests.post(f"{BOOKING_SERVICE_URL}/showtimes", json=request.get_json())
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/showtimes/<date>", methods=['PUT'])
def update_showtime(date):
    """
    Update an existing showtime by date.

    Args:
        date (str): The date of the showtime to update.

    Returns:
        Response: JSON response with the updated showtime or an error message.
    """
    response = requests.put(f"{BOOKING_SERVICE_URL}/showtimes/{date}", json=request.get_json())
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/showtimes/<date>", methods=['DELETE'])
def delete_showtime(date):
    """
    Delete an existing showtime by date.

    Args:
        date (str): The date of the showtime to delete.

    Returns:
        Response: JSON response with the deleted showtime or an error message.
    """
    response = requests.delete(f"{BOOKING_SERVICE_URL}/showtimes/{date}")
    return make_response(jsonify(response.json()), response.status_code)


@app.route("/showmovies/<date>", methods=['GET'])
def get_showmovies_bydate(date):
    """
    Get details of a showtime by date.

    Args:
        date (str): The date of the showtime.

    Returns:
        Response: JSON response with the showtime details or an error message.
    """
    response = requests.get(f"{BOOKING_SERVICE_URL}/showmovies/{date}")
    return make_response(jsonify(response.json()), response.status_code)


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
