from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models.custom_user_models import CustomUser


class UserProfileAPIViewTest(APITestCase):
    """
    Test module for the UserProfileAPIView class.
    """

    def setUp(self):
        self.user_password = 'testpassword123'

        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password=self.user_password)

        self.url = reverse('user_profile', kwargs={'userid': self.user.pk})
        self.client.login(username='testuser', password=self.user_password)

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
        Ensure that a user can delete their own profile.
        """

        self.client.login(username='testuser', password='testpassword123')
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())
