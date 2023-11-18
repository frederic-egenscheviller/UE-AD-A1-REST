import json

import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'
SHOWTIME_SERVICE_URL = "http://localhost:3202"

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "Booking User ID not found"}), 400)


@app.route("/bookings", methods=['POST'])
def add_booking():
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
    req = request.get_json()
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            bookings.remove(booking)
            bookings.append(req)
            res = make_response(jsonify({"message": "booking updated"}), 200)
            return res
    return make_response(jsonify({"error": "no booking found with that user ID"}), 400)


@app.route("/bookings/<userid>", methods=['DELETE'])
def delete_booking_byuser(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            bookings.remove(booking)
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "no booking found with that user ID"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
