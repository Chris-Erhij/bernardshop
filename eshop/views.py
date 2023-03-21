from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.http import HttpRequest, HttpResponse


def product_list(request: HttpRequest, category_slug=None) -> HttpResponse:
    category = None
    categories = Category.objects.all()
    products: Product = Product.objects.filter(available=True)

    if category_slug:
        category: Category = get_object_or_404(Category, slug=category_slug)
        products: Product = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request: HttpRequest, id: str, slug: str) -> HttpResponse:
    product: Product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})
