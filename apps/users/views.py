from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .api.serializers import SignUpSerializer
from .models import CustomUser

#? 

class UserViewSet(ModelViewSet):
    # permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    
    def create(self, request):
        user_data = self.serializer_class(data=request.data)
        user_data.is_valid(raise_exception=True)

        CustomUser.objects.create(**user_data.validated_data)

        return Response(
            {'success': 'User created successfully'},
            status=status.HTTP_201_CREATED
        )




