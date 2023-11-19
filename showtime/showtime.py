import json

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Configuration
PORT = 3202
HOST = '0.0.0.0'

# Load initial schedule from a JSON file
with open('{}/databases/times.json'.format("."), "r") as jsf:
    schedule = json.load(jsf)["schedule"]


@app.route("/", methods=['GET'])
def home():
    """
    Home route to welcome users.

    Returns:
        str: Welcome message in HTML format.
    """
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"


@app.route("/showtimes", methods=['GET'])
def get_showtimes():
    """
    Retrieve all showtimes.

    Returns:
        Response: JSON response containing the schedule.
    """
    return make_response(jsonify(schedule), 200)


@app.route("/showtimes", methods=['POST'])
def create_showtime():
    """
    Create a new showtime.

    Returns:
        Response: JSON response with the new showtime or an error message.
    """
    req = request.get_json()

    if req["date"] not in [times["date"] for times in schedule]:
        schedule.append(req)
        return make_response(jsonify(req), 200)
    else:
        return make_response(jsonify({"error": "there is already a schedule for that date"}), 400)


@app.route("/showtimes/<date>", methods=['PUT'])
def update_showtime(date):
    """
    Update an existing showtime by date.

    Args:
        date (str): The date of the showtime to update.

    Returns:
        Response: JSON response with the updated showtime or an error message.
    """
    req = request.get_json()

    for times in schedule:
        if str(times["date"]) == str(date):
            times["date"] = req["date"]
            times["movies"] = req["movies"]
            return make_response(jsonify(req), 200)
    schedule.append(req)
    return make_response(jsonify(req), 400)


@app.route("/showtimes/<date>", methods=['DELETE'])
def delete_showtime(date):
    """
    Delete an existing showtime by date.

    Args:
        date (str): The date of the showtime to delete.

    Returns:
        Response: JSON response with the deleted showtime or an error message.
    """
    for times in schedule:
        if str(times["date"]) == str(date):
            schedule.remove(times)
            return make_response(jsonify(times), 200)
    return make_response(jsonify({"error": "no schedule found on that date"}), 400)


@app.route("/showtimes/<date>", methods=['GET'])
def get_showtime_bydate(date):
    """
    Get details of a showtime by date.

    Args:
        date (str): The date of the showtime.

    Returns:
        Response: JSON response with the showtime details or an error message.
    """
    for times in schedule:
        if str(times["date"]) == str(date):
            return make_response(jsonify(times["date"], times["movies"]), 200)
    return make_response(jsonify({"error": "No movie scheduled at this date"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
