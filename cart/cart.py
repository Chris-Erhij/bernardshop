from decimal import Decimal
from django.conf import settings
from eshop.models import Product
from django. http import HttpRequest
from typing import Any, Generator
import typing as ty
from coupon.models import Coupon


class Cart(object):
    def __init__(self, request: HttpRequest) -> None:
        """ Initialize the cart 
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Initialize an empty cart for session.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # Store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def coupon(self) -> Coupon | None:
        """Return a coupon object or None
        """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self) -> Decimal:
        """return the amount to be deducted from the total amount of cart items.

            If a coupon has been applied, which is then stored in the current session.
        """
        if self.coupon:
            return (self.coupon().discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    
    def get_total_price_after_discount(self) -> Decimal:
        """Return total amount of items in cart after deducting discount
        """
        return self.get_total_price() - self.get_discount()

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False) -> None:
        """Add a product to the cart or update it's quantity
        """ 
        product_id: str = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self) -> None:
        # Mark the session as modified to make sure it gets saved.
        self.session.modified = True

    def remove(self, product: Product) -> None:
        """Remove a product(s) from the cart.
        """
        product_id: str = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self) -> Generator[ty.Dict, Any, None]:
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
