from django.shortcuts import render




























@decorator.http.require_POST
def cart_detail_view(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    context: dict = {'cart': cart}
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/detail.html', context)

