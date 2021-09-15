import json
from typing import List
import requests
import requests_with_caching

# var for type hint
url: str
param: dict
movie_list: List
dic: dict
name: str
lst: List
response: requests.Response
data: dict


def get_movies_from_tastedive(name) -> dict:
    url = "https://tastedive.com/api/similar"
    param = {'q': name, 'type': 'movies', 'limit': 5}
    response = requests_with_caching.get(url, params=param)
    return json.loads(response.text)


def extract_movie_titles(dic) -> List:
    movie_list = [movie['Name'] for movie in dic['Similar']['Results']]
    return movie_list


def get_related_titles(lst) -> List:
    movie_list = [extract_movie_titles(get_movies_from_tastedive(movie)) for movie in lst]
    movie_list = [movie for sublst in movie_list for movie in sublst]
    # convert to a set to remove duplicates. convert back to list for the expected var type
    return list(set(movie_list))


def get_movie_data(name) -> dict:
    url = "http://www.omdbapi.com/"
    param = {'t': name, 'r': 'json'}
    response = requests_with_caching.get(url, params=param)
    return json.loads(response.text)


def get_movie_rating(dic) -> int:
    for data in dic['Ratings']:
        if data['Source'] == 'Rotten Tomatoes':
            return int(data['Value'][:-1])
    return 0


def get_sorted_recommendations(lst) -> List:
    dic = {}
    for name in get_related_titles(lst):
        dic[name] = get_movie_rating(get_movie_data(name))
    return [movie[0] for movie in sorted(dic.items(), key=lambda item: (item[1], item[0]), reverse=True)]


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better
# error messages
# get_movies_from_tastedive("Bridesmaids")
# get_movies_from_tastedive("Black Panther")
