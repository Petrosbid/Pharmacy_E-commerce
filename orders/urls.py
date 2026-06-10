from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('tracking/', views.tracking, name='tracking'),
    path('history/', views.order_history, name='history'),
]
