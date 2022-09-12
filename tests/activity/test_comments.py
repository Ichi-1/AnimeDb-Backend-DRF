import pytest
import requests
from faker import Faker

URL = "http://localhost:8000/api/comments/"
fake = Faker()

"""
Only three type of commentable object is allowed:
manga, anime, review
"""

def test_comment_anime_create(anime, api_client):
    comment_body = {
        "commentable_type": "anime",
        "commentable_id": anime.id,
        "body": fake.text()
    }
    create_comment = api_client.post(path=URL, data=comment_body)
    assert create_comment.status_code == 201

    comment_body["commentable_id"] = 1555
    create_comment = api_client.post(path=URL, data=comment_body)
    assert create_comment.status_code == 404


def test_comment_manga_create(manga, api_client):
    comment_body = {
        "commentable_type": "manga",
        "commentable_id": manga.id,
        "body": fake.text()
    }
    create_comment = api_client.post(path=URL, data=comment_body)
    assert create_comment.status_code == 201

    comment_body["commentable_id"] = 1555
    create_comment = api_client.post(path=URL, data=comment_body)
    assert create_comment.status_code == 404


def test_commentable_type_invalid(api_client):
    comment_body = {
        "commentable_type": "movie",
        "commentable_id": 1,
        "body": fake.text()
    }
    create_comment = api_client.post(path=URL, data=comment_body)
    error_text = str(create_comment.json())
    assert create_comment.status_code == 400
    assert '"movie" is not a valid choice.' in error_text


def test_comment_body_invalid(anime, api_client):
    comment_body = {
        "commentable_type": "anime",
        "commentable_id": anime.id,
        "body": 'haha'
    }
    create_comment = api_client.post(path=URL, data=comment_body)
    error_text = str(create_comment.json())
    assert create_comment.status_code == 400
    assert "Ensure this value has at least 20 characters" in error_text


def test_comment_json_invalid(api_client):
    create_comment = api_client.post(path=URL, data={})
    error_text = str(create_comment.json())
    assert create_comment.status_code == 400
    assert "This field is required" in error_text


def test_author_anonymous():
    response = requests.post(url=URL, data={"random": "random"})
    assert response.status_code == 401


def test_update_comment(api_client, comment_manga):
    comment_id = str(comment_manga.id)
    update_comment = api_client.patch(
        path=URL + comment_id + "/",
        data={'body': fake.text()}
    )
    assert update_comment.status_code == 200
