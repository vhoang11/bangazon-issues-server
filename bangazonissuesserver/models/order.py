from django.db import models
from .user import User

class Order(models.Model):
    """Model that represents an order"""
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=500)
    is_open = models.BooleanField()
    created_on = models.DateTimeField()
    order_total = models.DecimalField(max_digits=15, decimal_places=2)
    