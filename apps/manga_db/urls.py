from django.urls import path
from .router import manga_list_or_detail

app_name = 'manga_db'

urlpatterns = [
    
]

urlpatterns += manga_list_or_detail.urls