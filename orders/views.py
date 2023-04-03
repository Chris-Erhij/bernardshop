from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.http import HttpRequest, HttpResponse
from django import forms


def order_create(request: HttpRequest,) -> HttpResponse:
    cart = Cart(request)
    if request.method == 'POST':
        form: (forms.ModelForm | OrderCreateForm) = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
            cart.clear()
        return render(request, "orders/order/created.html", {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {'cart': cart, 'form': form})
