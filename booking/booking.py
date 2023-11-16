from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

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


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    req = request.get_json()

    for date in req["dates"]:
        showtime_response = requests.get(f"{SHOWTIME_SERVICE_URL}/showmovies/{date['date']}")
        for movie in date["movies"]:
            if movie not in showtime_response.json()[1]:
                return make_response(jsonify({"error": "one of selected movies is not available for these date"}), 409)

    bookings.append(req)
    res = make_response(jsonify({"message": "booking added"}), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
