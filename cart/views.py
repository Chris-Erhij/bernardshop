from django.shortcuts import render




























@decorator.http.require_POST
def cart_detail_view(request: HttpRequest, product_id: str) -> HttpResponse:
    cart = Cart(request)
    context: dict = {'cart': cart}
    return render(request, 'cart/detail.html', context)
d
