import json
import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
SHOWTIME_SERVICE_URL = "http://showtime:3202"

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    """
    Returns a welcome message for the Booking service.

    Returns:
        str: Welcome message in HTML format.
    """
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    """
    Retrieves all bookings in JSON format.

    Returns:
        Response: JSON response containing all bookings.
    """
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    """
    Retrieves booking information for a specific user by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing booking information or an error message.
    """
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(jsonify(booking), 200)
    return make_response(jsonify({"error": "Booking User ID not found"}), 400)


@app.route("/bookings", methods=['POST'])
def add_booking():
    """
    Adds a new booking based on the JSON request.

    Returns:
        Response: JSON response containing the new booking information or an error message.
    """
    req = request.get_json()

    if req["userid"] not in [booking["userid"] for booking in bookings]:
        for date in req["dates"]:
            showtime_response = requests.get(f"{SHOWTIME_SERVICE_URL}/showmovies/{date['date']}")
            for movie in date["movies"]:
                if movie not in showtime_response.json()[1]:
                    return make_response(jsonify({"error": "one of selected movies is not available for these date"}),
                                         409)
        bookings.append(req)
        return make_response(jsonify(req), 200)
    else:
        return make_response(jsonify({"error": "booking already exists for this user"}), 400)


@app.route("/bookings/<userid>", methods=['PUT'])
def update_booking_byuser(userid):
    """
    Updates booking information for a specific user by user ID based on the JSON request.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing the updated booking information or an error message.
    """
    req = request.get_json()

    for date in req["dates"]:
        showtime_response = requests.get(f"{SHOWTIME_SERVICE_URL}/showmovies/{date['date']}")
        for movie in date["movies"]:
            if movie not in showtime_response.json()[1]:
                return make_response(jsonify({"error": "one of selected movies is not available for these date"}),
                                     409)

    if req["userid"] not in [booking["userid"] for booking in bookings]:
        bookings.append(req)
        return make_response(jsonify(req), 200)
    else:
        for booking in bookings:
            if str(booking["userid"]) == str(userid):
                booking["dates"] = req["dates"]
                return make_response(jsonify(req), 200)


@app.route("/bookings/<userid>", methods=['DELETE'])
def delete_booking_byuser(userid):
    """
    Deletes a booking for a specific user by user ID.

    Args:
        userid (str): User ID.

    Returns:
        Response: JSON response containing the deleted booking information or an error message.
    """
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            bookings.remove(booking)
            return make_response(jsonify(booking), 200)
    return make_response(jsonify({"error": "no booking found with that user ID"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
