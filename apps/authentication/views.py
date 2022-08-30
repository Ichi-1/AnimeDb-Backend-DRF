from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .providers.google import GoogleService
from .providers.github import GitHubService
from .serializers import (
    GoogleLoginSerializer, GitHubLoginSerializer, SignUpSerializer
)


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    """I refusede to use custom ModelViewSet because
    i dont want to handling all steps of activation process.
    Instead use Djoser package.
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


class GoogleLoginAPIView(GenericAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        UserModel = CustomUser.objects
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id_token = serializer.validated_data["id_token"]
        id_token_valid = GoogleService.validate_id_token(user_id_token)

        if not id_token_valid:
            return Response(
                {"detail": "Could not verify token signature"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        candidate = UserModel.filter(email=id_token_valid["email"])
        if candidate.exists():
            tokens = UserModel.get_tokens(candidate.first())
            return Response(
                {"tokens": tokens},
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = UserModel.create_social_user(
                provider="google",
                user_data=id_token_valid
            )
            return Response(
                {
                    "detail": "Accoun created",
                    "tokens": social_user_tokens
                },
                status=status.HTTP_201_CREATED
            )
        except AuthenticationFailed:
            return Response(
                {"detail": "Social Account Creation Failed"},
                status=status.HTTP_409_CONFLICT
            )


class GitHubLoginAPIView(GenericAPIView):
    """
    If code in POST request is valid - will signed up user
    with given social provider data (login, email),
    and then autorize him with jwt tokens pair.
    If user already registred with this email -
    autorize him in existed account with jwt tokens pair

    """
    serializer_class = GitHubLoginSerializer

    def post(self, request):
        UserModel = CustomUser.objects
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        """
        Making POST request with temporary code to GitHub OAuth App,
        as response - json with user data
        """
        response = GitHubService.get_access_token(code)

        if 'error' in response:
            return Response(
                {
                    'error': response['error'],
                    'detail': response['error_description']
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = response.get('access_token')
        user_info = GitHubService.get_user_info(access_token)

        if user_info['email'] is None or 'email' not in user_info:
            return Response(
                {'detail': 'Cannot create account without providing public email'},
                status=status.HTTP_409_CONFLICT
            )

        candidate = UserModel.filter(email=user_info["email"])
        if candidate.exists():
            tokens = UserModel.get_tokens(candidate.first())
            return Response(
                {"tokens": tokens},
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = UserModel.create_social_user(
                provider="github",
                user_data=user_info
            )
            return Response(
                {
                    "detail": "Accoun created",
                    "tokens": social_user_tokens
                },
                status=status.HTTP_201_CREATED
            )
        except AuthenticationFailed:
            return Response(
                {"detail": "Social Account Creation Failed"},
                status=status.HTTP_409_CONFLICT
            )
