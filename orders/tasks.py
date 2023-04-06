from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id) -> int:
    """Task to send an e-mail notification concurrently.

        Only when an order is successfully created.
    """
    order: Order = Order.objects.get(id=order_id)
    subject: str = F"Order nr {order.id}"
    message: str = F"Dear {order.first_name},\n\n"\
                   F"You have successfully placed an order"\
                   F"Your order ID is {order.id}."
    mail_sent: int = send_mail(
        subject=subject,
        message=message,
        from_email='christianerhijotah@gmail.com',
        recipient_list=[order.email,]
    )
    return mail_sent
