import requests

URL = "http://localhost:8000/api/anime/"
cowboy_bebop_id = "1/"

def test_get_anime_list():
    response = requests.get(url=URL)
    assert response.status_code == 200


def test_get_anime_detail():
    response = requests.get(url=URL + cowboy_bebop_id)
    assert response.status_code == 200
    assert response.json()['title'] == 'Cowboy Bebop'
    

def test_get_anime_comments_list():
    response = requests.get(url=URL + cowboy_bebop_id + "comments/")
    assert response.status_code == 200


def test_get_anime_reviews_list():
    response = requests.get(url=URL + cowboy_bebop_id + "reviews/")
    assert response.status_code == 200


def test_anime_title(anime):
    assert anime.title == 'Cowboy Bebop'