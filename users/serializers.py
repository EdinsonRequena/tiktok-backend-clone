from typing import Any, Dict

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model with custom fields.

    This serializer is used for creating and updating User instances.
    It includes fields such as id, username, email, password, bio, and profile_picture.
    The password field is write-only, meaning it is not included in the serialized representation
    when sending data to the client.

    Methods:
    - create(validated_data: Dict[str, Any]) -> User:
    Creates a new User instance based on the validated data.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'bio', 'profile_picture']
        extra_kwargs: Dict[str, Dict[str, Any]] = {
            'password': {'write_only': True}
        }

    def create(self, validated_data: Dict[str, Any]) -> User:
        user: User = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        return user
