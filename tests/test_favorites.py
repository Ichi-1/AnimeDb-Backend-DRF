import requests

URL = "http://localhost:8000/api/anime/"


def test_update_user_favorites(api_client, anime):
    add_favorites = api_client.put(path=URL + f"{anime.id}/favorites/")
    add_again = api_client.put(path=URL + f"{anime.id}/favorites/")
    error_text = str(add_again.json())

    assert add_favorites.status_code == 200
    assert add_again.status_code == 409
    assert f"'{anime.title}' already added to favorites" in str(error_text)


def test_user_favorites_401(anime):
    response = requests.put(url=URL + f"{anime.id}/favorites/")
    assert response.status_code == 401


def test_delete_user_favorites(api_client, anime):
    api_client.put(path=URL + f"{anime.id}/favorites/")  # simulate put request, add to favorites
    delete_favorites = api_client.delete(path=URL + f"{anime.id}/favorites/")

    assert delete_favorites.status_code == 204
