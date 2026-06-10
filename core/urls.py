from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('consultation/', views.consultation, name='consultation'),
    path('faq/', views.faq, name='faq'),
    path('returns/', views.returns, name='returns'),
    path('privacy/', views.privacy, name='privacy'),
    path('contact/', views.contact, name='contact'),
]
