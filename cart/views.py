from django.shortcuts import render, redirect, get_object_or_404
from eshop.models import Product
from cart.forms import CartAddProductForm
from cart import Cart
from django.views import decorators
from django.http import (
    HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse
)
from django import forms


@decorators.http.require_POST
def add_to_cart_view(request: HttpRequest, product_id: str) -> (HttpResponseRedirect | HttpResponsePermanentRedirect):
    cart = Cart(request)  # Upon request create an empty form instance.
    product: Product = get_object_or_404(Product, id=product_id)
    form: (forms.Form | CartAddProductForm) = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail_view')

@decorators.http.require_POST
def remove_from_cart_view(request: HttpRequest, product_id: str) -> (HttpResponseRedirect | HttpResponsePermanentRedirect):
    cart = Cart(request)
    product: Product = get_object_or_404(Product, id=product_id)
    if product in cart:
        cart.remove(product=product)
    return redirect('cart:cart_detail_view')
from django.shortcuts import render




























@decorator.http.require_POST
def cart_detail_view(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    context: dict = {'cart': cart}
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/detail.html', context)

