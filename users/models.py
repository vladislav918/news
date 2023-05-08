from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from posts.models import News


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    avatar = models.ImageField(
        upload_to='photo_users/',
        verbose_name='Фото',
        null=True,
        blank=True
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


