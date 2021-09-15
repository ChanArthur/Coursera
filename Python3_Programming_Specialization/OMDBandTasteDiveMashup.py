import requests_with_caching
import json

def get_movies_from_tastedive(name):
    url = "https://tastedive.com/api/similar"
    param = {'q': name, 'type': 'movies', 'limit': 5}
    response = requests_with_caching.get(url, params=param)
    return json.loads(response.text)

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_movies_from_tastedive("Bridesmaids")
get_movies_from_tastedive("Black Panther")