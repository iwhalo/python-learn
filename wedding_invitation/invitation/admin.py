from django.contrib import admin
from .models import WeddingEvent, Guest, GalleryImage, PageVisit


@admin.register(WeddingEvent)
class WeddingEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'bride_name', 'groom_name', 'event_date', 'venue', 'created_at']
    list_filter = ['event_date', 'created_at']
    search_fields = ['title', 'bride_name', 'groom_name', 'venue']
    date_hierarchy = 'event_date'
    ordering = ['-created_at']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'invitation_code', 'rsvp_status', 'guest_count', 'get_total_guests', 'created_at']
    list_filter = ['rsvp_status', 'created_at', 'guest_count']
    search_fields = ['name', 'phone', 'email', 'invitation_code']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'phone', 'email', 'invitation_code')
        }),
        ('RSVP信息', {
            'fields': ('rsvp_status', 'guest_count', 'message')
        }),
        ('系统信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_total_guests(self, obj):
        """
        显示该宾客确认出席的总人数
        """
        return obj.get_total_guests_count()
    get_total_guests.short_description = '实际出席人数'
    get_total_guests.admin_order_field = 'guest_count'
    
    def get_queryset(self, request):
        """
        优化查询，减少数据库查询次数
        """
        queryset = super().get_queryset(request)
        return queryset.select_related()


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'visit_count', 'last_visited']
    list_filter = ['page_name', 'last_visited']
    search_fields = ['page_name']
    ordering = ['-last_visited']
    readonly_fields = ['visit_count', 'last_visited']