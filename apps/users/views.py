from apps.authentication.models import CustomUser
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    UserListSerializer, 
    UserMeRetrieveSerializer, 
    UserMeUpdateSerializer
)
from .mixins import MixedPermissionModelViewSet


class UserViewSet(MixedPermissionModelViewSet):
    """
    GET /users/ - retrieve list of registred users;
    GET /users/:id - retrieve users public profile;
    PATCH /users/:id - partial updating of user profile. Authenticated Only;
    """
    queryset = CustomUser.objects.all().order_by('-last_login')
    parser_classes = [FormParser, MultiPartParser]


    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action == 'update':
            return UserMeUpdateSerializer
        if self.action == 'retrieve':
            return UserMeRetrieveSerializer



