import pytest
from faker import Faker
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import (
    CommentFactory,
    UserFactory,
    AnimeFactory,
    MangaFactory,
    CommentMangaFactory
)


register(UserFactory)
register(AnimeFactory) # => anime_factory
register(MangaFactory)
register(CommentMangaFactory)

fake = Faker()

@pytest.fixture
def anime(db, anime_factory):
    return anime_factory.create()

@pytest.fixture
def manga(db, manga_factory):
    return manga_factory.create()

@pytest.fixture
def user(db, user_factory):
    return user_factory.create()

@pytest.fixture
def comment_manga(db, comment_manga_factory):
    return comment_manga_factory.create()


@pytest.fixture
def api_client(db, user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'JWT {refresh.access_token}')
    return client

