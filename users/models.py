from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(unique=True, max_length=10)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(
        default='default/profile.png', upload_to='profile_pics', blank=True)
    connection = models.ManyToManyField(
        "self", blank=True, related_name="connection")

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + " " + self.last_name
