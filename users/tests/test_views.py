from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


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


class UserProfileAPIViewTest(APITestCase):
    """
    Test module for the UserProfileAPIView class.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='testpassword123')
        self.url = reverse('user_profile', kwargs={'userid': self.user.pk})

        self.update_data = {
            'bio': 'Updated bio',
        }

    def test_retrieve_user_profile(self):
        """
        Ensure that a user profile can be retrieved by user ID.
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_user_profile(self):
        """
        Ensure that a user profile can be updated by user ID.
        """

        response = self.client.put(self.url, self.update_data, format='json')

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.bio, 'Updated bio')

    def test_delete_user_profile(self):
        """
        Ensure that a user profile can be deleted by user ID.
        """

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())
