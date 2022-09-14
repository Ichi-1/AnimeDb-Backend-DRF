import requests
import pytest
from faker import Faker

URL = "http://localhost:8000/api/users/"
fake = Faker()


def test_get_users_list():
    response = requests.get(URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_user_public_profile(api_client):
    pass
