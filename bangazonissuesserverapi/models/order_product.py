from django.db import models
from .product import Product
from .order import Order

class OrderProduct(models.Model):
    """Model that represents a subscription"""
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quantity_total = models.DecimalField(max_digits=8, decimal_places=2)
