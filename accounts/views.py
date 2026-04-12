from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import FindPostcodeUserSerializer
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework.authentication import TokenAuthentication


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


class FindPostcodeLoginView(APIView):
    """
    Accepts a POST request with user credentials,
    and returns a signed token upon successful authentication.

    Returns:
        200 OK: Authentication successful, token included in response.
        400 Bad Request: Missing or invalid credentials.
        404 Not Found: No account associated.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [TokenAuthentication]
    queryset = UserModel.objects.all()

    @extend_schema(
        request=FindPostcodeUserSerializer,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.NONE,
            404: OpenApiTypes.NONE,
        }
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        check_user = UserModel.objects.filter(username=username).first()
        if not check_user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request=request, username=username, password=password)

        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        data = {
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
        }

        return Response(data, status=status.HTTP_200_OK)
