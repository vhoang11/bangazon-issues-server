from django.db import models
from .user import User
from .category import Category

class Product(models.Model):
    """Model that represents a product"""
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_on = models.DateTimeField()
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
