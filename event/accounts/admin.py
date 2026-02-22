from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'phone', 'date_of_birth', 'address', 'avatar', 
        'receive_notifications', 'receive_marketing_emails'
    ]


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'date_joined', 'booking_count'
    ]
    
    def booking_count(self, obj):
        count = obj.bookings.count()
        if count > 0:
            return format_html('<span style="color: green;">{} bookings</span>', count)
        return '0 bookings'
    booking_count.short_description = 'Bookings'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth', 'receive_notifications', 'created_at']
    list_filter = ['receive_notifications', 'receive_marketing_emails', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
