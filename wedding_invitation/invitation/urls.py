"""
婚礼邀请函应用的URL配置模块

这个模块定义了婚礼邀请函网站的所有URL路由模式，
将不同的URL路径映射到对应的视图函数。
每个路由都包含详细的注释，说明其功能和对应的视图函数。
"""

from django.urls import path  # 导入Django的URL路由函数
from . import views  # 导入当前应用的视图模块


# URL路由配置列表
# 定义应用的所有URL路由模式，按顺序匹配
urlpatterns = [
    # 首页路由
    # 将根路径(/)映射到index视图函数，显示婚礼邀请函主页面
    # name参数用于在模板中反向解析URL
    path('', views.index, name='index'),

    # RSVP表单页面路由
    # 将/rsvp/路径映射到rsvp_form视图函数，显示宾客回复表单
    # 宾客可以通过此表单回复是否参加婚礼
    path('rsvp/', views.rsvp_form, name='rsvp'),

    # RSVP提交处理路由
    # 将/submit-rsvp/路径映射到submit_rsvp视图函数，处理宾客回复表单提交
    # 此路由接收表单数据，验证并保存到数据库
    path('submit-rsvp/', views.submit_rsvp, name='submit_rsvp'),

    # 倒计时页面路由
    # 将/countdown/路径映射到countdown视图函数，显示婚礼倒计时
    # 页面会计算并显示距离婚礼还有多少天
    path('countdown/', views.countdown, name='countdown'),

    # 相册页面路由
    # 将/gallery/路径映射到gallery视图函数，显示婚礼照片画廊
    # 页面会展示所有上传的婚礼照片
    path('gallery/', views.gallery, name='gallery'),

    # 地图页面路由
    # 将/map/路径映射到map_location视图函数，显示婚礼地点地图
    # 页面使用高德地图API展示婚礼举办地点
    path('map/', views.map_location, name='map'),

    # 宾客列表页面路由
    # 将/guests/路径映射到guest_list视图函数，显示所有已回复的宾客信息
    # 页面会列出所有已确认参加的宾客及其详细信息
    path('guests/', views.guest_list, name='guest_list'),

    # 地图配置API路由
    # 将/api/map-config/路径映射到get_map_config视图函数，提供地图初始化配置的JSON接口
    # 此API用于获取地图配置信息，避免在前端暴露API密钥
    path('api/map-config/', views.get_map_config, name='get_map_config'),

    # 宾客统计API路由
    # 将/api/guest-stats/路径映射到guest_stats_api视图函数，提供宾客统计数据的JSON接口
    # 此API用于获取宾客统计信息，如总人数、已确认人数等
    path('api/guest-stats/', views.guest_stats_api, name='guest_stats_api'),
]