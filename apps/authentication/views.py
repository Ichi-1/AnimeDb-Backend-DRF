from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ..users.models import User
from .providers.google import GoogleService
from .providers.github import GitHubService
from .serializers import (
    GoogleLoginSerializer, GitHubLoginSerializer
)
from drf_spectacular.utils import extend_schema


# TODO переработать вью социальны провайдеров. Слишком много return
# TODO "post" has 5 returns that exceeds max allowed 3


class GoogleLoginAPIView(GenericAPIView):
    serializer_class = GoogleLoginSerializer

    @extend_schema(summary='Sign Up with Google OAuth2')
    def post(self, request):
        user_model = User.objects
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id_token = serializer.validated_data["id_token"]
        id_token_valid = GoogleService.validate_id_token(user_id_token)

        if not id_token_valid:
            return Response(
                {"detail": "Could not verify token signature"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        candidate = user_model.filter(email=id_token_valid["email"])
        if candidate.exists():
            tokens = user_model.get_tokens(candidate.first())
            return Response(
                {"tokens": tokens},
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = user_model.create_social_user(
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

    @extend_schema(summary="Sign Up with GitHub OAuth2")
    def post(self, request):
        user_model = User.objects
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

        candidate = user_model.filter(email=user_info["email"])
        if candidate.exists():
            tokens = user_model.get_tokens(candidate.first())
            return Response(
                {"tokens": tokens},
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = user_model.create_social_user(
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
