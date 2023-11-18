import json

import requests
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

MOVIE_SERVICE_URL = "http://localhost:3200"
BOOKING_SERVICE_URL = "http://localhost:3201"

with open('{}/databases/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/user/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "user ID not found"}), 400)


@app.route("/user", methods=['POST'])
def create_user():
    req = request.get_json()

    if req["id"] not in [user["id"] for user in users]:
        users.append(req)
        res = make_response(jsonify(req), 200)
        return res
    else:
        return make_response(jsonify({"error": "user already exists"}), 400)


@app.route("/user/<userid>", methods=['PUT'])
def update_user(userid):
    req = request.get_json()

    for user in users:
        if str(user["id"]) == str(userid):
            user.update(req)
            res = make_response(jsonify(req), 200)
            return res
    return make_response(jsonify({"error": "user ID not found"}), 400)


@app.route("/user/<userid>", methods=['DELETE'])
def delete_user(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "user ID not found"}), 400)


@app.route("/user-bookings/<userid>", methods=['GET'])
def get_user_bookings(userid):
    booking_response = requests.get(f"{BOOKING_SERVICE_URL}/bookings/{userid}")

    if booking_response.status_code == 200:
        user_bookings = booking_response.json()
        return make_response(jsonify(user_bookings), 200)
    else:
        return make_response(jsonify({"error": "user ID not found in Booking service"}), 400)


@app.route("/user-bookings/<userid>/detailed", methods=['GET'])
def get_detailed_userbookings(userid):
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
