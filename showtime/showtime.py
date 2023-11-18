import json

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

PORT = 3202
HOST = '0.0.0.0'

with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=['GET'])
def get_showtimes():
    return make_response(jsonify(schedule), 200)


@app.route("/showtimes", methods=['POST'])
def create_showtime():
    req = request.get_json()

    if req["date"] not in [times["date"] for times in schedule]:
        schedule.append(req)
        return make_response(jsonify(req), 200)
    else:
        return make_response(jsonify({"error": "there is already a schedule for that date"}), 400)


@app.route("/showtimes/<date>", methods=['PUT'])
def update_showtime(date):
    req = request.get_json()

    for times in schedule:
        if str(times["date"]) == str(date):
            schedule.remove(times)
            schedule.append(req)
            return make_response(jsonify(req), 200)
    return make_response(jsonify({"error": "no schedule found on that date"}), 400)


@app.route("/showtimes/<date>", methods=['DELETE'])
def delete_showtime(date):
    for times in schedule:
        if str(times["date"]) == str(date):
            schedule.remove(times)
            return make_response(jsonify(times), 200)
    return make_response(jsonify({"error": "no schedule found on that date"}), 400)


@app.route("/showtimes/<date>", methods=['GET'])
def get_showtime_bydate(date):
    for times in schedule:
        if str(times["date"]) == str(date):
            return make_response(jsonify(times["date"], times["movies"]), 200)
    return make_response(jsonify({"error": "No movie scheduled at this date"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
