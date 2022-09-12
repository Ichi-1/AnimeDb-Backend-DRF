import requests

URL = "http://localhost:8000/api/manga/"
berserk_id = "1/"

def test_get_manga_list():
    response = requests.get(url=URL)
    assert response.status_code == 200


def test_get_manga_detail():
    response = requests.get(url=URL + berserk_id)
    assert response.status_code == 200
    assert response.json()["title"] == "Berserk"


def test_get_manga_comments_list():
    response = requests.get(url=URL + berserk_id + "comments/")
    assert response.status_code == 200


def test_get_manga_reviews_list():
    response = requests.get(url=URL + berserk_id + "reviews/")
    assert response.status_code == 200