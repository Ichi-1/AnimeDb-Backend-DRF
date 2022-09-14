import pytest
from faker import Faker
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import (
    UserFactory,
    AnimeFactory,
    MangaFactory,
    MangaReviewFactory,
)

register(UserFactory)
register(AnimeFactory)  # => anime_factory
register(MangaFactory)
register(MangaReviewFactory)

fake = Faker()


@pytest.fixture(scope='function')
def auth_user(db, user_factory):
    """
    Simulate authorized user, which is perfoming CRUD actions
    """
    return user_factory.create(
        nickname="admin",
        email="admin@admin.com"
    )


@pytest.fixture(scope='function')
def someone(db, user_factory):
    """
    Simulates someone else users, who held resources
    """
    return user_factory.create(
        nickname=fake.name(),
        email=f'{fake.name()}@{fake.domain_name()}',
    )


@pytest.fixture
def anime(db, anime_factory):
    """
    Simulates instacne of Anime
    """
    return anime_factory.create()


@pytest.fixture
def manga(db, manga_factory):
    """
    Simulates instance of Manga
    """
    return manga_factory.create()


@pytest.fixture
def manga_review(db, manga_review_factory, auth_user):
    """
    Simulates review of "Berserk" manga created by "admin"
    """
    return manga_review_factory.create(
        author=auth_user
    )


@pytest.fixture
def someone_review(db, manga_review_factory, someone):
    """
    Simulates review of "Berserk" manga created by someone
    """
    return manga_review_factory.create(
        author=someone
    )


@pytest.fixture
def api_client(db, auth_user):
    """
    Fixture provide interface to requesting with Authorization header
    client.post(path='http://example.com, data={"payload":"you pretty good"})

    It use "auth_user" fixture
    """
    refresh = RefreshToken.for_user(auth_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'JWT {refresh.access_token}')
    return client
