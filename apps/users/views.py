from apps.authentication.models import CustomUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserListSerializer,
    UserMeRetrieveSerializer,
    UserMeUpdateSerializer
)
from .mixins import UserPermissionsViewSet


class UserViewSet(UserPermissionsViewSet):
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
        if self.action == 'partial_update':
            return UserMeUpdateSerializer
        if self.action == 'retrieve':
            return UserMeRetrieveSerializer

    def partial_update(self, request, *args, **kwargs):
        user_id = request.user.id
        user_to_update = kwargs['pk']

        if user_id != user_to_update:
            return Response(
                {'detail': 'You are not authorized to this action'},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return super().partial_update(request, args, kwargs)
