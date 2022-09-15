import requests
from faker import Faker


URL = "http://localhost:8000/api/reviews/"
fake = Faker()


def test_review_create(api_client, manga):
    review = {
        "reviewable_type": "manga",
        "reviewable_id": manga.id,
        "body": fake.text(),
        "santiment": "Negative"
    }
    create_review = api_client.post(path=URL, data=review)
    assert create_review.status_code == 201


def test_reviewable_type_invalid(api_client):
    review = {
        "reviewable_type": "movie",
    }
    invalid_reviewable_type = api_client.post(path=URL, data=review)
    error_text = str(invalid_reviewable_type.json())

    assert invalid_reviewable_type.status_code == 400
    assert '"movie" is not a valid choice.' in error_text


def test_reviewable_404(api_client):
    review = {
        "reviewable_type": "manga",
        "reviewable_id": 15555,
        "body": fake.text(),
        "santiment": "Negative"
    }
    reviewable_404 = api_client.post(path=URL, data=review)

    assert reviewable_404.status_code == 404


def test_review_body_invalid(api_client, manga):
    review = {
        "reviewable_type": "manga",
        "reviewable_id": manga.id,
        "body": 'haha',
        "santiment": "Negative"
    }
    invalid_body = api_client.post(path=URL, data=review)
    error_text = str(invalid_body.json())

    assert invalid_body.status_code == 400
    assert "Ensure this value has at least 100 characters" in error_text


def test_review_santiment_invalid(api_client, manga):
    review = {
        "reviewable_type": "manga",
        "reviewable_id": manga.id,
        "body": fake.text(),
        "santiment": "MARVELOUS"
    }
    invalid_santiment = api_client.post(path=URL, data=review)
    error_text = str(invalid_santiment.json())

    assert invalid_santiment.status_code == 400
    assert '"MARVELOUS" is not a valid choice.' in error_text


def test_review_author_anonymous():
    response = requests.post(url=URL)
    assert response.status_code == 401


def test_update_my_review(api_client, manga_review):
    update_my_review = api_client.patch(
        path=URL + str(manga_review.id) + "/",
        data={
            "body": fake.text() + fake.text(),
            "santiment": "Neutral"
        }
    )
    response_text = str(update_my_review.json())

    assert manga_review.author.nickname == 'admin'
    assert update_my_review.status_code == 200
    assert "Neutral" in response_text


def test_restrict_update_someone_review(api_client, someone_review):
    restrict_update = api_client.patch(
        path=URL + str(someone_review.id) + "/",
        data={"santiment": "Negative"}
    )

    assert restrict_update.status_code == 403
    assert someone_review.santiment == "Positive"


def test_delete_my_review(api_client, manga_review):
    delete_my_review = api_client.delete(
        path=URL + str(manga_review.id) + "/"
    )
    assert delete_my_review.status_code == 204


def test_restrict_delete_someone_review(api_client, someone_review):
    restrict_delete = api_client.delete(
        path=URL + str(someone_review.id) + "/"
    )
    assert restrict_delete.status_code == 403
