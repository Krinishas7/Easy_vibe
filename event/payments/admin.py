from django.contrib import admin
from django.utils.html import format_html
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'booking', 'amount', 'payment_method', 'status', 
        'esewa_transaction_id', 'created_at', 'completed_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = [
        'booking__booking_id', 'esewa_transaction_id', 'esewa_reference_id',
        'booking__user__username', 'booking__event__title'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('booking', 'amount', 'payment_method', 'status')
        }),
        ('eSewa Details', {
            'fields': ('esewa_transaction_id', 'esewa_reference_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['booking', 'amount']
        return self.readonly_fields
    
    actions = ['mark_completed', 'mark_failed']
    
    def mark_completed(self, request, queryset):
        for payment in queryset:
            if payment.status == 'pending':
                payment.mark_completed()
        self.message_user(request, 'Selected payments were marked as completed.')
    mark_completed.short_description = 'Mark selected payments as completed'
    
    def mark_failed(self, request, queryset):
        for payment in queryset:
            if payment.status == 'pending':
                payment.mark_failed()
        self.message_user(request, 'Selected payments were marked as failed.')
    mark_failed.short_description = 'Mark selected payments as failed'
