from django.urls import path
from . import views

app_name: str = 'payment'
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('completed/', views.payment_completed, name='completed'),
]
