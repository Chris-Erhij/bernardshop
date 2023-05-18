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
api_key: str = settings.PAYSTACK_SK
end_point: str = settings.PAYSTACK_ENDPOINT


def payment_process(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    # Retrieve the order ID set in django session (payment init I.e. "order_create view").
    order = get_object_or_404(Order, id=request.session.get('order_id', None))

    if request.method == 'POST':
        cancel_url = request.build_absolute_uri(reverse('payment:pay_canceled'))

        # Additional metadata paystack endpoint don't accept naturally.
        metadata: str = json.dumps({'order_id': order.id, 'cancel_url': cancel_url})

        # Paystack checkout session data.
        session_data: dict = {
            'amount': order.get_total_cost(),
            'email': order.email,
            'metadata': metadata,
        }
       
        headers: dict([str, any]) = {'Authorization': F"Bearer {api_key}", "Content-Type": "application/json"}

        # Api request to paystack server.
        response = requests.get(end_point, headers=headers, data=session_data)

        if response.status_code == 200:
            response_data = response.json()
            paystack_modal = response_data['data']['authorization_url']
            return redirect(paystack_modal, code=303)
        
        raise ConnectionError("Unknown error occured, please try again!") from BaseException
    return render(request, 'payment/pay_process.html', locals())


def payment_completed(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/pay_completed.html')


def payment_canceled(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/pay_canceled.html')
