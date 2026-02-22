from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Booking, Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ['ticket_id', 'qr_code', 'is_used', 'used_at']
    fields = ['attendee_name', 'attendee_email', 'ticket_id', 'qr_code', 'is_used', 'used_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_id', 'user', 'event', 'quantity', 'total_amount', 
        'status', 'created_at', 'payment_status'
    ]
    list_filter = ['status', 'created_at', 'event__category']
    search_fields = [
        'booking_id', 'user__username', 'user__email', 'event__title',
        'contact_name', 'contact_email'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'event', 'quantity', 'total_amount', 'status')
        }),
        ('Contact Details', {
            'fields': ('contact_name', 'contact_email', 'contact_phone')
        }),
        ('Payment', {
            'fields': ('payment_reference',)
        }),
    )
    
    readonly_fields = ['booking_id', 'total_amount']
    inlines = [TicketInline]
    
    def payment_status(self, obj):
        try:
            payment = obj.payment
            color_map = {
                'pending': 'orange',
                'completed': 'green',
                'failed': 'red',
                'refunded': 'blue'
            }
            color = color_map.get(payment.status, 'gray')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, payment.get_status_display()
            )
        except:
            return format_html('<span style="color: red;">No Payment</span>')
    payment_status.short_description = 'Payment Status'
    
    actions = ['mark_confirmed', 'mark_cancelled']
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings were confirmed.')
    mark_confirmed.short_description = 'Mark selected bookings as confirmed'
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings were cancelled.')
    mark_cancelled.short_description = 'Mark selected bookings as cancelled'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'ticket_id', 'booking', 'attendee_name', 'event_title', 
        'is_used', 'used_at', 'qr_code_preview'
    ]
    list_filter = ['is_used', 'booking__status', 'created_at']
    search_fields = [
        'ticket_id', 'attendee_name', 'attendee_email', 
        'booking__booking_id', 'booking__event__title'
    ]
    readonly_fields = ['ticket_id', 'qr_code_preview']
    
    def event_title(self, obj):
        return obj.booking.event.title
    event_title.short_description = 'Event'
    
    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="100" height="100" />',
                obj.qr_code.url
            )
        return 'No QR Code'
    qr_code_preview.short_description = 'QR Code'
