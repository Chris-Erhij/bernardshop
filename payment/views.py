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
import requests
import json

# Create paystack instance.
api_key: str = settings.PAYSTACK_SECRET_KEY
end_point: str = settings.PAYSTACK_ENDPOINT


def payment_process(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    # Retrieve the order ID set in django session (payment init I.e. "order_create view").
    order = get_object_or_404(Order, id=request.session.get('order_id', None))

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:pay_completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:pay_canceled'))

        # Additional metadata paystack endpoint don't accept naturally.
        metadata: dict = json.dump({'client_reference_id': order.id, 'cancel_url': cancel_url})

        # Paystack checkout session data.
        session_data: dict = {
            'mode': 'payment',
            'success_url': success_url,
            'metadata': metadata,
            'line_items': []
        }
        # Populate session data line_Items.
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'ghs',
                'product_data': {
                        'name': item.product.name,
                                },
                    },
                'quantity': item.quantity,
            })
        headers: dict([str, str]) = {'authorization': F"Bearer {api_key}"}

        # Api request to paystack server.
        r = requests.post(end_point, headers=headers, data=session_data)
        response = r.json()

        if response['status'] == True:
            try:
                end_point_url = response['data']['authorization_url']
                return redirect(end_point_url, code=303)
            except Exception:
                raise("Authorization error!")
        return render(request, 'orders/order/created.html', locals())
    return render(request, 'orders/order/created.html', locals())


def payment_completed(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/pay_completed.html')


def payment_canceled(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/pay_canceled.html')
