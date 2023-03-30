from django.contrib import admin
from .models import Order, OrderItem
from typing import Type


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields: list([str, ...]) = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display: list([str, ...]) = [
        'id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 
        'created', 'updated'
    ]

    list_filter: list([str, ...]) = [
        'paid', 'created', 'updated'
    ]
    inlines: list([Type]) = [OrderItemInline]
