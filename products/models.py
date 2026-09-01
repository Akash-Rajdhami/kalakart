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


class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    address = models.TextField()

    phone = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"