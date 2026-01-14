"""
Django管理员界面配置模块

这个模块定义了婚礼邀请函应用中所有模型在Django管理后台的显示方式和配置，
包括列表显示、搜索、过滤、排序等功能。每个模型管理器都经过精心设计，
提供直观的管理界面和高效的数据操作方式。
"""

from django.contrib import admin  # 导入Django管理后台模块
from .models import WeddingEvent, Guest, GalleryImage, PageVisit  # 导入应用中的所有模型


@admin.register(WeddingEvent)
class WeddingEventAdmin(admin.ModelAdmin):
    """
    婚礼事件模型管理器

    管理婚礼的基本信息，包括标题、新娘姓名、新郎姓名、
    婚礼日期和场地等信息。提供了丰富的列表显示、搜索和过滤功能，
    使管理员能够高效地管理婚礼事件数据。

    配置特性：
    - 显示关键信息字段
    - 按日期和创建时间过滤
    - 多字段搜索功能
    - 日期层次导航
    - 按创建时间倒序排列
    """
    # 列表页面显示的字段
    # 选择最关键的信息字段，便于快速浏览
    list_display = ['title', 'bride_name', 'groom_name', 'event_date', 'venue', 'created_at']

    # 右侧过滤器
    # 允许按婚礼日期和创建时间筛选记录
    list_filter = ['event_date', 'created_at']

    # 搜索字段
    # 支持在标题、新人姓名和场地中搜索
    search_fields = ['title', 'bride_name', 'groom_name', 'venue']

    # 日期层次导航
    # 提供按年、月、日导航的日期层次结构
    date_hierarchy = 'event_date'

    # 默认排序：按创建时间倒序
    # 最新的记录显示在顶部
    ordering = ['-created_at']


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    """
    宾客模型管理器

    管理宾客信息，包括姓名、联系方式、邀请码、
    RSVP状态和出席人数等。提供了自定义方法显示实际出席人数，
    并优化了查询性能，提高管理效率。

    配置特性：
    - 显示宾客基本信息和出席统计
    - 多维度过滤功能
    - 全面的搜索支持
    - 字段分组显示
    - 自定义方法显示实际出席人数
    - 优化的查询性能
    """
    # 列表页面显示的字段
    # 包含自定义方法get_total_guests显示实际出席人数
    list_display = ['name', 'phone', 'email', 'invitation_code', 'rsvp_status', 'guest_count', 'get_total_guests', 'created_at']

    # 右侧过滤器
    # 支持按RSVP状态、创建时间和出席人数过滤
    list_filter = ['rsvp_status', 'created_at', 'guest_count']

    # 搜索字段
    # 支持在姓名、联系方式和邀请码中搜索
    search_fields = ['name', 'phone', 'email', 'invitation_code']

    # 日期层次导航
    # 提供按年、月、日导航的日期层次结构
    date_hierarchy = 'created_at'

    # 默认排序：按创建时间倒序
    # 最新的记录显示在顶部
    ordering = ['-created_at']

    # 只读字段
    # 创建时间不允许手动修改
    readonly_fields = ['created_at']

    # 字段分组显示
    # 将字段分为基本信息、RSVP信息和系统信息三组
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'phone', 'email', 'invitation_code')
        }),
        ('RSVP信息', {
            'fields': ('rsvp_status', 'guest_count', 'message')
        }),
        ('系统信息', {
            'fields': ('created_at',),
            'classes': ('collapse',)  # 可折叠
        }),
    )

    def get_total_guests(self, obj):
        """
        自定义方法：显示该宾客确认出席的总人数

        在管理后台列表中显示实际的出席人数统计，便于管理员快速了解
        确认出席的宾客总数。此方法调用模型的get_total_guests_count方法。

        Args:
            obj: Guest模型实例

        Returns:
            int: 实际出席人数
        """
        return obj.get_total_guests_count()

    # 设置方法在列表中的显示名称
    get_total_guests.short_description = '实际出席人数'

    # 设置方法在列表中的排序字段
    get_total_guests.admin_order_field = 'guest_count'

    def get_queryset(self, request):
        """
        重写查询集：优化查询性能

        使用select_related减少数据库查询次数，提高页面加载速度。
        虽然Guest模型没有外键关系，但此方法预留了未来扩展的可能性，
        并展示了性能优化的最佳实践。

        Args:
            request: HttpRequest对象

        Returns:
            QuerySet: 优化后的查询集
        """
        queryset = super().get_queryset(request)
        return queryset.select_related()


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """
    相册图片模型管理器

    管理婚礼相关的照片和图片，包括标题、
    图片文件和上传时间等信息。提供了直观的图片管理界面，
    支持按标题和描述搜索，以及按上传时间过滤。

    配置特性：
    - 显示图片标题和缩略图
    - 按上传时间过滤
    - 支持标题和描述搜索
    - 日期层次导航
    - 按上传时间倒序排列
    """
    # 列表页面显示的字段
    # 显示标题、图片和上传时间
    list_display = ['title', 'image', 'uploaded_at']

    # 右侧过滤器
    # 允许按上传时间筛选记录
    list_filter = ['uploaded_at']

    # 搜索字段
    # 支持在标题和描述中搜索
    search_fields = ['title', 'description']

    # 日期层次导航
    # 提供按年、月、日导航的日期层次结构
    date_hierarchy = 'uploaded_at'

    # 默认排序：按上传时间倒序
    # 最新的图片显示在顶部
    ordering = ['-uploaded_at']


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    """
    页面访问统计模型管理器

    管理各个页面的访问统计信息，
    用于分析网站的访问情况。提供了直观的访问数据展示，
    支持按页面名称和最后访问时间过滤，以及按页面名称搜索。

    配置特性：
    - 显示页面名称、访问次数和最后访问时间
    - 多维度过滤功能
    - 页面名称搜索支持
    - 按最后访问时间倒序排列
    - 只读字段保护（不允许手动修改统计数据）
    """
    # 列表页面显示的字段
    # 显示页面名称、访问次数和最后访问时间
    list_display = ['page_name', 'visit_count', 'last_visited']

    # 右侧过滤器
    # 允许按页面名称和最后访问时间筛选记录
    list_filter = ['page_name', 'last_visited']

    # 搜索字段
    # 支持在页面名称中搜索
    search_fields = ['page_name']

    # 默认排序：按最后访问时间倒序
    # 最近访问的页面显示在顶部
    ordering = ['-last_visited']

    # 只读字段（不允许手动修改）
    # 访问次数和最后访问时间由系统自动更新，不允许手动修改
    readonly_fields = ['visit_count', 'last_visited']