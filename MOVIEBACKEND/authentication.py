from functools import wraps
from flask import request, jsonify
from config import TMDB_API_KEY

def authenticate_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-Api-Key")  # Update header key to match the request
        print("API Key:", api_key)  # Print API key for debugging
        print("Request Headers:", request.headers)  # Print request headers for debugging

        if not api_key or api_key != TMDB_API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper
