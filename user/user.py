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


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)