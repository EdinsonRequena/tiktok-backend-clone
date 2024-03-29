import shutil

from django.conf import settings
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models.custom_user_models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Tests for the CustomUser model.

    Ensures that the CustomUser model is created correctly with all additional fields
    functioning as expected.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            bio='A bio here',
            profile_picture=SimpleUploadedFile(
                name='test_image.jpg',
                content=b'file_content',
                content_type='image/jpeg'
            )
        )

    def test_user_creation(self):
        """
        Confirm that the user is created correctly.
        """

        self.assertEqual(self.user.username, 'testuser')

    def test_user_email(self):
        """
        Confirm that the user's email is set correctly.
        """

        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_bio(self):
        """
        Confirm that the user's bio is set correctly.
        """

        self.assertEqual(self.user.bio, 'A bio here')

    def test_user_profile_picture(self):
        """
        Confirm that the user's profile picture is set correctly.
        """

        self.assertTrue(
            self.user.profile_picture.name.endswith('test_image.jpg'))

    def test_email_unique(self):
        """
        Confirm that the 'email' field is unique across the CustomUser model.
        Attempts to create a user with an email that's already in use should raise an exception.
        """
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                username='testuser2',
                email='testuser@example.com',
                password='testpass123'
            )

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
