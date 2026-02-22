from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<slug:slug>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<uuid:booking_id>/', views.booking_detail, name='booking_detail'),
    path('cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('download-tickets/<uuid:booking_id>/', views.download_tickets, name='download_tickets'),
    path('scanner/', views.qr_scanner, name='qr_scanner'),
    path('scanner/guide/', views.scanner_guide, name='scanner_guide'),
    path('api/verify-ticket/', views.verify_ticket_api, name='verify_ticket_api'),
    path('api/mark-ticket-used/', views.mark_ticket_used, name='mark_ticket_used'),
    
]
