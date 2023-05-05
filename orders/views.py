from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django import forms
from .tasks import order_created


def order_create(request: HttpRequest,) -> HttpResponse | HttpResponseRedirect:
    cart = Cart(request)
    if request.method == 'POST':
        form: (forms.ModelForm | OrderCreateForm) = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            cart.clear()

            order_created.delay(order_id=order.id)  # Asynchronous task.

            # Set the order in the session. 
            request.session['order_id'] = order.id
            # Redirect for payment.
            return redirect(reverse('payment:pay_process'))
    else:
        form = OrderCreateForm()
    return render(request, "orders/order/create.html", {'cart': cart, 'form': form})
