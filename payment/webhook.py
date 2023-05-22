import stripe
from orders.models import Order
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    """Listen for and handle stripe webhook events in real time.
    """
    event = None
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    payload = request.body
    
    # Construct stripe event.
    try:
        event = stripe.webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as ve:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as sve:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle event
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order: Order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            # Mark order as paid
            order.paid = True
            order.save()
    return HttpResponse(status=200)
