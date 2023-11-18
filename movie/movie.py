import json

from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)


@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)


@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res


@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "movie ID not found"}), 400)


@app.route("/moviesratingbetterthan/<rate>", methods=['GET'])
def get_movie_with_rating_better_than(rate):
    movies_json_list = []

    for movie in movies:
        if float(movie["rating"]) > float(rate):
            movies_json_list.append(movie)

    if movies_json_list:
        res = make_response(jsonify(movies_json_list), 200)
        return res
    return make_response(jsonify({"error": "movie with rate better than " + str(rate) + " not found"}), 400)


@app.route("/moviesbytitle/<movietitle>", methods=['GET'])
def get_movie_bytitle(movietitle):
    for movie in movies:
        if str(movie["title"]) == str(movietitle):
            return make_response(jsonify(movie), 200)

    return make_response(jsonify({"error": "movie title not found"}), 400)


@app.route("/movies", methods=['POST'])
def create_movie():
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(req["id"]):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify(req), 200)
    return res


@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


@app.route("/movies/<movieid>", methods=['PUT'])
def update_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie.update(req)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res


@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
