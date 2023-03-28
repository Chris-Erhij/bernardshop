from django.shortcuts import render, redirect, get_object_or_404
from eshop.models import Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.views.decorators.http import require_POST
from django.http import (
    HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
)
from django import forms
from django.urls import reverse


@require_POST
def cart_add(request: HttpRequest, product_id: str) -> (HttpResponseRedirect | HttpResponsePermanentRedirect):
    cart = Cart(request)  # Upon request create an empty cart instance.
    product: Product = get_object_or_404(Product, id=product_id)
    form: (forms.Form | CartAddProductForm) = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return HttpResponseRedirect(reverse('cart:cart_detail'))


@require_POST
def cart_remove(request: HttpRequest, product_id: str) -> (HttpResponseRedirect | HttpResponsePermanentRedirect):
    cart = Cart(request)
    product: Product = get_object_or_404(Product, id=product_id)
    if product in cart:
        cart.remove(product=product)
    return HttpResponseRedirect(reverse('cart:cart_detail'))


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})
