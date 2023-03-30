from django.db import models
from django.db.models import (
    Model, CharField, EmailField, BooleanField, DecimalField, DateTimeField, 
    PositiveIntegerField, ForeignKey, Index,
)
from .models import Product


class Order(Model):
    first_name: CharField = models.CharField(name="First name", max_length=50, help_text="Your last name here")
    last_name: CharField = models.CharField(name="Last name", max_length=50, help_text="Your first name here", )
    email: EmailField = models.EmailField(help_text="Enter your email here")
    address: CharField = models.CharField(max_length=250)
    postal_code: CharField = models.CharField(name="Postal code", max_length=50)
    city: CharField = models.CharField(max_length=100)
    created: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: DateTimeField = models.DateTimeField(auto_now=True)
    paid: BooleanField = models.BooleanField(default=False)

    class Meta:
        ordering: list([str]) = ['-created']
        indexes: list([Index[str]]) = [
            models.Index(fields=['-created',])
        ]

    def __str__(self) -> str:
        return F"Order {self.id}"
    
    def get_total_cost(self) -> int:
        return sum(item.get_cost for item in self.items.all())
    

class OrderItem(Model):
    order: ForeignKey = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product: ForeignKey = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price: DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    quantity: PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.id)
    
    def get_cost(self) -> int:
        return self.price * self.quantity
