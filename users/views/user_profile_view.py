from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpRequest

from utils import logger_config
from users.serializers import CustomUserSerializer
from users.models.custom_user_models import CustomUser
from users.constants import USER_WITH_ID_NOT_FOUND, USER_NOT_FOUND_MESSAGE


logger = logger_config.configure_logger()


class UserProfileAPIView(APIView):
    """
    API view for retrieving, updating, and deleting user profiles.

    Methods:
    - get: Retrieve a user profile by user ID.
    - put: Update a user profile by user ID.
    - delete: Delete a user profile by user ID.
    """

    def get(self, request: HttpRequest, userid: int) -> Response:  # pylint: disable=unused-argument
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
            logger.error(USER_WITH_ID_NOT_FOUND, userid)
            return Response({'error': USER_NOT_FOUND_MESSAGE}, status=status.HTTP_404_NOT_FOUND)

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
                return Response(
                    {'message': 'User has been updated successfully.',
                        'data': serializer.data, },
                    status.HTTP_200_OK,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            logger.error(USER_WITH_ID_NOT_FOUND, userid)
            return Response({'error': USER_NOT_FOUND_MESSAGE}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: HttpRequest, userid: int) -> Response:  # pylint: disable=unused-argument
        """
        Deletes a user with the given userid.

        Args:
            request (HttpRequest): The HTTP request object.
            userid (int): The id of the user to be deleted.

        Returns:
            Response: The HTTP response indicating the success or failure of the deletion.
        """
        # TODO: Add a check to ensure that the user is deleting their own profile.
        try:
            user = CustomUser.objects.get(pk=userid)
            user.delete()
            return Response(
                {'message': 'User has been deleted successfully.'},
                status=status.HTTP_204_NO_CONTENT
            )

        except CustomUser.DoesNotExist:
            logger.error(USER_WITH_ID_NOT_FOUND, userid)
            return Response({'error': USER_NOT_FOUND_MESSAGE}, status=status.HTTP_404_NOT_FOUND)
