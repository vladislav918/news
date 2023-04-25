from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/', verbose_name='Фото', null=True, blank=True)
