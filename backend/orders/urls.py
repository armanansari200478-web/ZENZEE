from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history_view, name='order_history'),
    path('<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('payment/success/', views.payment_success, name='payment_success'),
]
