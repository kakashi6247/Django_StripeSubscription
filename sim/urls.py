from django.urls import path
from .views import *

urlpatterns = [
    path('', subscribe, name='subscribe'),  # Subscription page
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
]