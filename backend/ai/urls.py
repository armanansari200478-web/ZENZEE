from django.urls import path
from . import views

urlpatterns = [
    path('stylist/', views.ai_stylist_view, name='ai_stylist'),
    path('api/query/', views.ai_query_api, name='ai_query_api'),
]
