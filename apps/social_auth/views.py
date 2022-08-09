from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleAuthSerializer
from .providers.google import GoogleService
from .services import create_social_account, grant_access_social_account
from apps.authentication.models import CustomUser


class GoogleLoginAPIView(GenericAPIView):
    serializer_class = GoogleAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id_token = serializer.validated_data['id_token']
        id_token_valid = GoogleService.validate_id_token(user_id_token)
        candidate = CustomUser.objects.filter(email=id_token_valid['email'])

        if not id_token_valid:
            return Response(
                {'detail': 'id_token is invalid. Could not verify token signature'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        

        if candidate.exists():
            token_pair = grant_access_social_account(candidate.first())
            return Response({
                    'username': id_token_valid['name'], 
                    'tokens':token_pair
                }, 
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = create_social_account('google', id_token_valid)
            return Response({
                    'username': id_token_valid['name'],
                    'tokens': social_user_tokens, 
                },
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {
                    "detail": "Social Account Creation Failed"
                }, 
                status=status.HTTP_400_BAD_REQUEST              
            )