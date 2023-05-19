from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.urls import reverse
from django.conf import settings
from decimal import Decimal
from orders.models import Order
from django.http import (
    HttpRequest, HttpResponseRedirect, HttpResponse
)
import stripe


# Stripe API key
stripe.api_key: str = settings.STRIPE_SK
stripe.api_version: str = settings.STRIPE_API_VERSION


def payment_process(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """Redirect to stripe payment process modal"""


    # Retrieve the order ID set in django session (payment init I.e. "order_create view").
    order: Order = get_object_or_404(Order, id=request.session.get('order_id', None))

    if request.method == 'POST':
        # Callback URLs
        cancel_url: str = request.build_absolute_uri(reverse('payment:pay_canceled'))
        callback_url: str = request.build_absolute_uri(reverse('payment:pay_completed'))

        # Checkout session data.
        metadata: dict = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': callback_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }
        # Add order items to checkout session.
        for item in order.items.all():
            metadata['line_items'].append({
            'price_data': {
                'unit_amount': int(item.price * Decimal('100')),
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
            },
            'quantity': item.quantity,
            })

        # Create checkout session.
        session = stripe.checkout.Session.create(**metadata)
        if session:
            try:
                return redirect(session.url, code=303)
            except:
                raise stripe.max_network_retries
        return render(request, 'payment/pay_process.html', locals())
    return render(request, 'payment/pay_process.html', locals())


def payment_completed(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/pay_completed.html')


def payment_canceled(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/pay_canceled.html')
