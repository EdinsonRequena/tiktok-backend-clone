from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import HttpRequest

from users.serializers import CustomUserSerializer


class RegisterUserAPIView(APIView):
    """
    API view for registering a new user.

    Methods:
    - post: Register a new user with the provided data.

    Returns:
    - Response: The HTTP response object containing the serialized user data if the registration
      is successful, or the validation errors if the provided data is invalid.
    """

    def post(self, request: HttpRequest) -> Response:
        """
        Handle HTTP POST request to create a new user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = self._create_user(serializer)
            refresh = RefreshToken.for_user(user)
            res_data = {
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(res_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _create_user(serializer):
        """
        Creates a new user based on the provided serializer.

        Args:
            serializer: The serializer containing the user data.

        Returns:
            The created user object.
        """
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return user
