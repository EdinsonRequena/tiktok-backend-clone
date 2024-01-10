from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import HttpRequest
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from utils import logger_config

from users.models import CustomUser
from users.serializers import CustomUserSerializer

logger = logger_config.configure_logger()


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
            serializer.validated_data['password'] = make_password(
                serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    """
    API view for user login.

    This view handles the POST request for user login. It expects the 'username' and 'password'
    fields in the request data.

    Methods:
    - post(request: HttpRequest) -> Response: Handles the POST request for user login.

    Returns:
    - Response: The HTTP response object containing the refresh and access tokens if
      the login is successful, or an error message if the provided credentials are invalid.
    """

    def post(self, request: HttpRequest) -> Response:
        """
        Handle the HTTP POST request to authenticate a user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the authentication tokens if successful,
            or an error message if the credentials are invalid.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    """
    API view for retrieving, updating, and deleting user profiles.

    Methods:
    - get: Retrieve a user profile by user ID.
    - put: Update a user profile by user ID.
    - delete: Delete a user profile by user ID.
    """

    def get(self, request: HttpRequest, userid: int) -> Response:
        """
        Retrieve a user by their ID.

        Args:
            request (HttpRequest): The HTTP request object.
            userid (int): The ID of the user to retrieve.

        Returns:
            Response: The serialized user data if found,
            or a 404 response if the user does not exist.
        """

        try:
            user = CustomUser.objects.get(pk=userid)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            logger.error("User with ID %s does not exist.", userid)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request: HttpRequest, userid: int) -> Response:
        """
        Update a user's information.

        Args:
            request (HttpRequest): The HTTP request object.
            userid (int): The ID of the user to be updated.

        Returns:
            Response: The HTTP response containing the updated user data or an error message.
        """
        try:
            user = CustomUser.objects.get(pk=userid)
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User has been updated successfully.'}, , status=status.HTTP_200_OK, serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            logger.error("User with ID %s does not exist.", userid)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: HttpRequest, userid: int) -> Response:
        """
        Deletes a user with the given userid.

        Args:
            request (HttpRequest): The HTTP request object.
            userid (int): The id of the user to be deleted.

        Returns:
            Response: The HTTP response indicating the success or failure of the deletion.
        """
        try:
            user = CustomUser.objects.get(pk=userid)
            user.delete()

            return Response({'message': 'User has been deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            logger.error("User with ID %s does not exist.", userid)
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
