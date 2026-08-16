from django.urls import path
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
]
