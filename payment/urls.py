from django.urls import path
from . import views

app_name: str = 'payment'
urlpatterns = [
    path('process/', views.payment_process, name='pay_process'),
    path('canceled/', views.payment_canceled, name='pay_canceled'),
    path('completed/', views.payment_completed, name='pay_completed'),
]
