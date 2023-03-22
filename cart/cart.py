from decimal import Decimal
from django.conf import settings
from eshop.models import Product
from django. http import HttpRequest
from typing import Any


class Cart(object):
    def __init__(self, request: HttpRequest):
        """
            Initialize the cart 
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: int, quantity: int = 1, override_quantity: bool = False) -> None:
        """
            Add a product to the cart or update it's quantity
        """
        product_id: str = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['qunatity'] += quantity
        self.save()

    def save(self) -> None:
        # Mark the session as modified to make sure it gets saved.
        self.session.modified = True

    def remove(self, product: int) -> Any:
        """
            Remove a product(s) from the cart.
        """
        product_id: str = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self) -> None:
        """Iterate over the items in the cart and get the products from the database.
        """
        product_ids: str = self.cart.keys()
        products: Product = Product.objects.filter(id__in=product_ids)  # Get product objects and add them to cart
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self) -> int:
        """Return total price of items in the cart
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self) -> None:
        # Remove cart from session.
        del self.session[settings.CART_SESSION_ID]
        self.save()
