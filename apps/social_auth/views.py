from apps.authentication.models import CustomUser
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .providers.google import GoogleService
from .providers.github import GitHubService
from .serializers import GoogleLoginSerializer, GitHubLoginSerializer
from .services import create_social_account, grant_access_social_account


class GoogleLoginAPIView(GenericAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id_token = serializer.validated_data["id_token"]
        id_token_valid = GoogleService.validate_id_token(user_id_token)

        if not id_token_valid:
            return Response(
                {"detail": "id_token is invalid. Could not verify token signature"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        candidate = CustomUser.objects.filter(email=id_token_valid["email"])
        if candidate.exists():
            token_pair = grant_access_social_account(candidate.first())
            return Response(
                {"tokens": token_pair}, 
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = create_social_account("google", id_token_valid)
            return Response(
                {"tokens": social_user_tokens},
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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]
        """
        Make POST with temporary code to GitHub OAuth App,
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

        if user_info['email'] == None or 'email' not in user_info:
            return Response(
                {'detail': 'Cannot create account without providing public email'},
                status=status.HTTP_409_CONFLICT
            )


        candidate = CustomUser.objects.filter(email=user_info["email"])
        if candidate.exists():
            token_pair = grant_access_social_account(candidate.first())
            return Response(
                {"tokens": token_pair}, 
                status=status.HTTP_201_CREATED
            )

        try:
            social_user_tokens = create_social_account("github", user_info)
            return Response(
                {"tokens": social_user_tokens}, 
                status=status.HTTP_201_CREATED
            )
        except AuthenticationFailed:
            return Response(
                {"detail": "Social Account Creation Failed"},
                status=status.HTTP_409_CONFLICT
            )
