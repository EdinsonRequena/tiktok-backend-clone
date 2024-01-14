from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models.custom_user_models import CustomUser


class LoginUserAPIViewTest(APITestCase):
    """
    Test module for the LoginUserAPIView class.
    """

    url = reverse('login_user')

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com')
        self.user.set_password('testpassword123')
        self.user.save()

        self.valid_credentials = {
            'username': 'testuser',
            'password': 'testpassword123',
        }

        self.invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

    def test_login_with_valid_credentials(self):
        """
        Ensure that a user can login with valid credentials.
        """

        response = self.client.post(self.url, self.valid_credentials)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_login_with_invalid_credentials(self):
        """
        Ensure that a user cannot login with invalid credentials.
        """

        response = self.client.post(self.url, self.invalid_credentials)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
