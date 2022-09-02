from rest_framework.routers import SimpleRouter
from .views import MangaViewSet

manga_list_or_detail = SimpleRouter()
manga_list_or_detail.register(r'manga', MangaViewSet, basename='manga')

