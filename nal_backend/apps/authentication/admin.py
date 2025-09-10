from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DeviceSession

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'role', 'is_verified', 'is_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'phone']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('uuid', 'phone', 'role', 'is_verified', 'two_factor_enabled')
        }),
    )
    readonly_fields = ['uuid', 'created_at', 'updated_at']

@admin.register(DeviceSession)
class DeviceSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_id', 'device_type', 'is_active', 'last_used']
    list_filter = ['device_type', 'is_active', 'created_at']
    search_fields = ['user__email', 'device_id']