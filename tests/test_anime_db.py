import requests
import pytest
from apps.activity.models import Comment
from apps.anime_db.models import AnimeReview
from faker import Faker


URL = "http://localhost:8000/api/anime/"
cowboy_bebop_id = "1/"

fake = Faker()


def test_get_anime_list():
    response = requests.get(url=URL)
    assert response.status_code == 200


def test_get_anime_detail():
    response = requests.get(url=URL + cowboy_bebop_id)
    assert response.status_code == 200
    assert response.json()['title'] == 'Cowboy Bebop'


@pytest.mark.django_db
def test_get_anime_comments_list(api_client, auth_user, anime):
    Comment.objects.bulk_create([
        Comment(
            author=auth_user, body=fake.text(),
            commentable=anime, commentable_id=anime.id,
        ),
        Comment(
            author=auth_user, body=fake.text(),
            commentable=anime, commentable_id=anime.id,
        )
    ])

    response = api_client.get(path=URL + f"{anime.id}/comments/")
    result = response.json()["result"]

    assert response.status_code == 200
    assert result != []


@pytest.mark.django_db
def test_get_anime_reviews_list(api_client, auth_user, anime):
    AnimeReview.objects.create(
        author=auth_user,
        anime=anime,
        body=fake.text() * 2,
        santiment='Positive'
    )
    AnimeReview.objects.create(
        author=auth_user,
        anime=anime,
        body=fake.text() * 2,
        santiment='Negative'
    )

    response = api_client.get(path=URL + f"{anime.id}/reviews/")
    result = response.json()["result"]

    assert response.status_code == 200
    assert result != []
