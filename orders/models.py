from django.db import models
from django.db.models import (
    Model, CharField, EmailField, BooleanField, DecimalField, DateTimeField, 
    PositiveIntegerField, ForeignKey, Index, IntegerField
)
from eshop.models import Product
from typing import Type
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from coupon.models import Coupon


class Order(Model):
    first_name: CharField = models.CharField(max_length=50,)
    last_name: CharField = models.CharField(max_length=50,)
    email: EmailField = models.EmailField()
    address: CharField = models.CharField(max_length=250)
    postal_code: CharField = models.CharField(max_length=50)
    city: CharField = models.CharField(max_length=100)
    created: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: DateTimeField = models.DateTimeField(auto_now=True)
    ref: CharField = models.CharField(max_length=200)
    paid: BooleanField = models.BooleanField(default=False)

    coupon: ForeignKey = models.ForeignKey(Coupon, null=True, blank=True, related_name='orders',
                                           on_delete=models.SET_NULL)
    discount: IntegerField = models.IntegerField(default=0, validators=[MinValueValidator(0), 
                                                                        MaxValueValidator(100)])
    

    class Meta:
        ordering: list([str]) = ['-created']
        indexes: list([Type]) = [
            Index(fields=['-created',])
        ]

    def __str__(self) -> str:
        return F"Order {self.id}"
    
    def get_total_before_discount(self) -> int:
        """Return total cost of an order before applying discount
        """
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self) -> Decimal:
        """Return the discount stored for an order if any exit
        """
        if self.discount:
            return (self.get_total_before_discount() * (self.discount / Decimal(100)))
        return Decimal(0)
    
    def get_total_cost(self) -> Decimal:
        """Return total cost of an order after applying discount
        """
        return self.get_total_before_discount() - self.get_discount()
    

class OrderItem(Model):
    order: ForeignKey = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product: ForeignKey = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price: DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    quantity: PositiveIntegerField = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return str(self.id)
    
    def get_cost(self) -> int:
        return self.price * self.quantity
