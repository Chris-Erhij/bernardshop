from .cart import Cart
from django.http import HttpRequest


def cart(request: HttpRequest) -> dict:  # Context processor
    """Return dictionary of a cart instance.

        Dictionary is to be added/set into Django's "requestContext", which is loaded everytime
        from the added "Template settings".
    """
    return {'cart': Cart(request)}
