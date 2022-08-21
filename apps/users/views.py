from apps.authentication.models import CustomUser
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import UserListSerializer


class UserListView(mixins.ListModelMixin, 
                  viewsets.GenericViewSet):
    """
    Return list of all registred user 
    sorted by: last_login, desc.
    """
    queryset = CustomUser.objects.all()\
        .order_by('-last_login')\

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer


        
