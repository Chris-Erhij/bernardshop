from django.urls import path
from . import views

app_name: str = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('detail/<int:product_id>/', views.cart_add, name='cart_add'),
    path('detail/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
