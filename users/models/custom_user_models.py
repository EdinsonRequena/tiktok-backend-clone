from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_("bio"), max_length=500, blank=True)
    profile_picture = models.ImageField(
        _("profile picture"), upload_to='profile_pictures/', null=True, blank=True)
