from django import forms
from django.forms import Form, TypedChoiceField, BooleanField

PRODUCT_QUANTITY_CHOICES: list([tuple[int, str]]) = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(Form):
    quantity: TypedChoiceField = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override: BooleanField = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
