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
import paystack


paystack.api_key: str = settings.PAYSTACK_SECRET_KEY
def payment_process(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_uri(reverse('payment:completed'))
        cancel_url = request.build_uri(reverse('payment:canceled'))

        # Paystack checkout session data.
        session_data: dict = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        for item in order.items.all():
            session_data['lines_items'].append({
                'price_date': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'ghs',
                        'product_data': {
                                    'name': item.product.name,
                                },
                    },
                'quantity': item.quantity,
            })

        # Create paystack checkout session
        session = paystack.checkout.session.create(**session_data)
        # Redirect to paystack payment form.
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/competed.html')


def payment_canceled(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/canceled.html')
