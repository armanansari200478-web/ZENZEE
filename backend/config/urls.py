"""
URL configuration for ZENZEE project.
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from accounts import views as account_views

urlpatterns = [
    path('health', lambda request: HttpResponse('ok')),
    path('health/', lambda request: HttpResponse('ok'), name='health'),

    path('admin/', admin.site.urls),
    path('', account_views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('ai/', include('ai.urls')),
    path('dashboard/', include('dashboard.urls')),

    # Direct media serving for production (Railway) when DEBUG=False
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
