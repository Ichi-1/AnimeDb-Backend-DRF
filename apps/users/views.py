from rest_framework import status
from apps.authentication.models import CustomUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import UserListSerializer


class UserViewSet(mixins.ListModelMixin, 
                  viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        return Response(serializer.data)
    
