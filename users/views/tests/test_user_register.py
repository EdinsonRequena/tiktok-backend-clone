from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models.custom_user_models import CustomUser


class RegisterUserAPIViewTest(APITestCase):
    """
    Test module for the RegisterUserAPIView class.
    """

    url = reverse('register_user')

    def setUp(self):
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpassword123',
            'bio': 'This is a bio'
        }
        self.invalid_data = {
            'username': '',
            'email': 'newuser@example.com',
            'password': 'testpassword123',
            'bio': 'This is a bio'
        }

    def test_user_registration_with_valid_data(self):
        """
        Ensure that a user can be registered with valid data.
        """

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'newuser')

    def test_user_receives_token_upon_registration(self):
        """
        Ensure that a user receives a token upon registration.
        """

        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_user_registration_with_invalid_data(self):
        """
        Ensure that a user cannot be registered with invalid data.
        """

        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_username(self):
        """
        Ensure that a user cannot be registered with a username that already exists.
        """

        self.client.post(self.url, self.valid_data)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
