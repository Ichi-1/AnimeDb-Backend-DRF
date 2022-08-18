from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import SignUpSerializer
from .models import CustomUser
from rest_framework.response import Response


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    """I refusede to use custom ModelViewSet because 
    i dont want to handling all steps of activation process.
    Instead use djoser package. 
    View just for test example.
    """ 

    def create(self, request):
        user = self.serializer_class(data=request.data)
        user.is_valid(raise_exception=True)
        CustomUser.objects.create_user(**user.validated_data)

        headers = self.get_success_headers(user.data)
        return Response(
            {"succes": "Activation link was sended"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

