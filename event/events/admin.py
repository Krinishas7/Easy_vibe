from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    prepopulated_fields = {'name': ('name',)}

    def event_count(self, obj):
        count = obj.events.count()
        if count > 0:
            url = reverse('admin:events_event_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} events</a>', url, count)
        return '0 events'
    event_count.short_description = 'Events'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'organizer', 'venue', 'start_date', 
        'status', 'tickets_sold_display', 'revenue_display', 'image_preview'
    ]
    list_filter = ['status', 'category', 'start_date', 'created_at']
    search_fields = ['title', 'description', 'venue', 'organizer__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'organizer', 'status')
        }),
        ('Event Details', {
            'fields': ('venue', 'address', 'start_date', 'end_date', 'image')
        }),
        ('Ticketing', {
            'fields': ('total_tickets', 'available_tickets', 'price')
        }),
    )
    
    readonly_fields = ['available_tickets']
    
    def tickets_sold_display(self, obj):
        sold = obj.tickets_sold
        total = obj.total_tickets
        percentage = (sold / total * 100) if total > 0 else 0
        
        color = 'green' if percentage > 70 else 'orange' if percentage > 30 else 'red'
        return format_html(
            '<span style="color: {};">{}/{} ({}%)</span>',
            color, sold, total, round(percentage, 1)
        )
    tickets_sold_display.short_description = 'Tickets Sold'
    
    def revenue_display(self, obj):
        revenue = obj.tickets_sold * obj.price
        return f'Rs. {revenue:,.2f}'
    revenue_display.short_description = 'Revenue'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Image'
    
    actions = ['make_published', 'make_draft', 'make_cancelled']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} events were successfully published.')
    make_published.short_description = 'Mark selected events as published'
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} events were moved to draft.')
    make_draft.short_description = 'Mark selected events as draft'
    
    def make_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} events were cancelled.')
    make_cancelled.short_description = 'Mark selected events as cancelled'
