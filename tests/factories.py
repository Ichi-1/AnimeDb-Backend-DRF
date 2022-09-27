import factory
from faker import Faker
from apps.anime.models import Anime, MyAnimeList
from apps.manga.models import Manga, MangaReview
from apps.users.models import User
from datetime import datetime


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class AnimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Anime

    id = 1
    age_rating = "R+"
    age_rating_guide = "Adult Only"
    average_rating = 85
    description = fake.text()
    episode_count = 85
    episode_length = 24
    kind = "TV"
    poster_image = "example.com"
    season = "Winter"
    staff = fake.text()
    studio = "DEEN"
    tags = fake.text()
    title = "Cowboy Bebop"
    title_jp = "Cowboy Bebop_jp"
    total_length = 230
    voice_actors = fake.text()
    year = 1999
    year_end = 2001


class MangaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manga

    id = 15
    author = fake.name()
    average_rating = 98
    chapters = 12
    description = fake.text()
    media_type = "manga"
    poster_image = "example.com"
    status = "status"
    tags = "tags"
    title = "Berserk"
    title_jp = "Berserk_jp"
    volumes = 15
    year_end = datetime.now()
    year_start = datetime.now()


class MangaReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MangaReview

    author = factory.SubFactory(UserFactory)
    body = fake.text()
    santiment = 'Positive'
    created_at = datetime.now()
    updated_at = datetime.now()
    manga = factory.SubFactory(MangaFactory)


class MyAnimeListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyAnimeList

    user  = factory.SubFactory(UserFactory)
    score = 4
    note = fake.text()
    updated_at = datetime.now()
    anime = factory.SubFactory(AnimeFactory)
    status = "Watching"
    num_episodes_watched = 21
