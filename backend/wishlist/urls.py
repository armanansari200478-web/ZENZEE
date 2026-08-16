from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('toggle/<int:product_id>/', views.wishlist_toggle_view, name='wishlist_toggle'),
]
