from django.db import models
from accounts.models import CustomUser


class Product(models.Model):

    CATEGORY_CHOICES = (
        ('Painting', 'Painting'),
        ('Handicraft', 'Handicraft'),
        ('Jewelry', 'Jewelry'),
        ('Pottery', 'Pottery'),
        ('Wooden Art', 'Wooden Art'),
        ('Traditional Wear', 'Traditional Wear'),
    )

    seller = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to='products/'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name