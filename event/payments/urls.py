from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<uuid:booking_id>/', views.initiate_payment, name='initiate_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('failure/', views.payment_failure, name='payment_failure'),
    path('webhook/', views.esewa_webhook, name='esewa_webhook'),
    path('status/<uuid:booking_id>/', views.payment_status, name='payment_status'),
]
