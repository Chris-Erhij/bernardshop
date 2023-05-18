from django.shortcuts import render, redirect, get_object_or_404
from eshop.models import Product
from .forms import CartAddProductForm
from coupon.forms import CouponApplyForm
from .cart import Cart
from django.views.decorators.http import require_POST
from django.http import (
    HttpRequest, HttpResponseRedirect, HttpResponse,
)
from django import forms


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    cart = Cart(request)
    product: Product = get_object_or_404(Product, id=product_id)
    form: (forms.Form | CartAddProductForm) = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart-detail')


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    cart = Cart(request)
    product: Product = get_object_or_404(Product, id=product_id)
    if product in cart:
        cart.remove(product=product)
    return redirect('cart:cart-detail')


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form})
