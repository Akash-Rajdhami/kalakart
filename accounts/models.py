from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    USER_TYPE = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE,
        default='customer'
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username