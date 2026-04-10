from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from accounts.serializers import FindPostcodeUserSerializer
from rest_framework.response import Response


UserModel = get_user_model()

class UserCreate(CreateAPIView):
    """
    Register a new user.

    Creates a new user account and returns an authentication token.
    The token should be included in subsequent requests as:
    `Authorization: Token <token_key>`
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = FindPostcodeUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
