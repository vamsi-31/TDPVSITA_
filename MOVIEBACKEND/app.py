from flask import Flask, Blueprint, request, jsonify
import requests
from config import TMDB_API_KEY
from authentication import authenticate_request

# Create Flask application
app = Flask(__name__)

# API Blueprint
api_blueprint = Blueprint("api", __name__)

# Movie Data Integration
def get_movie_details(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie = data["results"][0]
            movie_details = {
                "title": movie["title"],
                "release_year": movie["release_date"].split("-")[0],
                "plot": movie["overview"],
                # Include additional relevant details
            }
            return movie_details

    return None

def get_movie_list():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movie_list = []
        for movie in data["results"]:
            movie_list.append({
                "title": movie["title"],
                "release_year": movie["release_date"].split("-")[0],
                # Include additional relevant details
            })
        return movie_list

    return []

# API Endpoints
@api_blueprint.route("/movies/", methods=["GET"])
@authenticate_request
def get_movie_details_endpoint():
    movie_name = request.args.get("name")
    if not movie_name:
        return jsonify({"error": "Movie name is missing"}), 400

    movie_details = get_movie_details(movie_name)
    if not movie_details:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify(movie_details)

@api_blueprint.route("/movies", methods=["GET"])
@authenticate_request
def get_movie_list_endpoint():
    movie_list = get_movie_list()
    return jsonify(movie_list)

# Register API Blueprint
app.register_blueprint(api_blueprint)

# Run Flask application
if __name__ == "__main__":
    app.run(debug=True)
