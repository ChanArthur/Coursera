import json
from typing import List
import requests
import requests_with_caching


def get_movies_from_tastedive(name: str) -> dict:
    url: str = "https://tastedive.com/api/similar"
    param: dict = {'q': name, 'type': 'movies', 'limit': 5}
    response: requests.Response = requests_with_caching.get(url, params=param)
    return json.loads(response.text)


def extract_movie_titles(dic: dict) -> List:
    movie_list: List = [movie['Name'] for movie in dic['Similar']['Results']]
    return movie_list


def get_related_titles(lst: List) -> List:
    movie_list: List = [extract_movie_titles(get_movies_from_tastedive(movie)) for movie in lst ]
    movie_list = [movie for sublst in movie_list for movie in sublst]
    # convert to a set to remove duplicates. convert back to list for the expected var type
    return list(set(movie_list))


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better
# error messages
get_movies_from_tastedive("Bridesmaids")
get_movies_from_tastedive("Black Panther")
