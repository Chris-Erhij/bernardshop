from django.forms import ModelForm
from .models import Order
from typing import Type


class OrderCreateForm(ModelForm):
    class Meta:
        model: Type = Order
        fields: list([str, ...]) = [
            'first_name', 'last_name', 'email', 'address', 'postal_code', 'city'
        ]
