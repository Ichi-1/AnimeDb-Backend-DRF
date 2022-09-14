import pytest
import requests
from faker import Faker
from apps.activity.models import Comment

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


def test_comment_review_create(manga_review, api_client):
    comment_body = {
        "commentable_type": "review",
        "commentable_id": manga_review.id,
        "body": fake.text()
    }
    create_comment = api_client.post(path=URL, data=comment_body)
    assert create_comment.status_code == 201


def test_commentable_type_invalid(api_client):
    comment_body = {
        "commentable_type": "movie",
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


@pytest.mark.django_db
def test_update_my_comment(api_client, auth_user, manga, anime):
    my_comment_manga = Comment.objects.create(
        author=auth_user,
        body=fake.text(),
        commentable=manga
    )
    my_comment_anime = Comment.objects.create(
        author=auth_user,
        body=fake.text(),
        commentable=anime
    )

    update_comment_manga = api_client.patch(
        path=URL + str(my_comment_manga.id) + "/",
        data={"body": fake.text()}
    )
    update_comment_anime = api_client.patch(
        path=URL + str(my_comment_anime.id) + "/",
        data={"body": fake.text()}
    )

    update_comment_404 = api_client.patch(
        path=URL + '23232' + "/",
        data={"body": fake.text()}
    )

    assert update_comment_manga.status_code == 200
    assert update_comment_anime.status_code == 200
    assert update_comment_404.status_code == 404


@pytest.mark.django_db
def test_restrict_update_someone_comment(api_client, someone, manga):
    someone_comment = Comment.objects.create(
        author=someone,
        body=fake.text(),
        commentable=manga
    )
    restrict_update = api_client.patch(
        path=URL + str(someone_comment.id) + "/",
        data={"body": fake.text()}
    )
    error_text = str(restrict_update.json())

    assert "You are not authorized to this action" in error_text
    assert restrict_update.status_code == 403


@pytest.mark.django_db
def test_delete_my_comment(api_client, auth_user, manga):
    my_comment = Comment.objects.create(
        author=auth_user,
        body=fake.text(),
        commentable=manga
    )
    delete_comment = api_client.delete(
        path=URL + str(my_comment.id) + "/"
    )
    delete_comment_404 = api_client.delete(
        path=URL + '23232' + "/",
        data={"body": fake.text()}
    )

    assert delete_comment_404.status_code == 404
    assert delete_comment.status_code == 204


@pytest.mark.djang_db
def test_restrict_delete_someone_comment(api_client, someone, manga):
    someone_comment = Comment.objects.create(
        author=someone,
        body=fake.text(),
        commentable=manga
    )
    restrict_delete = api_client.delete(
        path=URL + str(someone_comment.id) + "/"
    )
    error_text = str(restrict_delete.json())

    assert "You are not authorized to this action" in error_text
    assert restrict_delete.status_code == 403
