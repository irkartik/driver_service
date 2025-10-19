from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """
    Admin interface for Driver model.
    """
    list_display = [
        'driver_id',
        'name',
        'phone',
        'vehicle_type',
        'vehicle_plate',
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_active',
        'vehicle_type',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'phone',
        'vehicle_plate'
    ]
    
    readonly_fields = [
        'driver_id',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('driver_id', 'name', 'phone')
        }),
        ('Vehicle Information', {
            'fields': ('vehicle_type', 'vehicle_plate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    
    actions = ['activate_drivers', 'deactivate_drivers']
    
    def activate_drivers(self, request, queryset):
        """
        Custom action to activate selected drivers.
        """
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} driver(s) activated successfully.')
    activate_drivers.short_description = 'Activate selected drivers'
    
    def deactivate_drivers(self, request, queryset):
        """
        Custom action to deactivate selected drivers.
        """
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} driver(s) deactivated successfully.')
    deactivate_drivers.short_description = 'Deactivate selected drivers'

