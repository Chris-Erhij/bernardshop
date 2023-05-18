from django import forms
from django.forms import Form, CharField


# A form to apply coupons to orders.
class CouponApplyForm(Form):
    code: CharField = forms.CharField()
