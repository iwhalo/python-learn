"""
URL configuration for wedding_invitation project.

婚礼邀请函项目URL配置文件
此文件定义了项目的URL路由规则，将URL映射到相应的视图函数或类

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # 导入Django管理后台模块
from django.urls import path, include  # 导入URL路由函数和include函数
from django.conf import settings  # 导入项目设置
from django.conf.urls.static import static  # 导入静态文件服务函数

# URL模式列表
# 定义项目的URL路由规则，按顺序匹配
urlpatterns = [
    # 管理后台URL路由
    # 将/admin/路径映射到Django管理后台
    path('admin/', admin.site.urls),

    # 婚礼邀请函应用URL路由
    # 将根路径(/)及其子路径映射到invitation应用的urls.py文件中定义的路由
    path('', include('invitation.urls')),
]

# 添加媒体文件服务配置
# 仅在DEBUG模式下启用媒体文件服务
# 生产环境中应由Web服务器(如Nginx)处理媒体文件
if settings.DEBUG:
    # 添加媒体文件URL路由，将MEDIA_URL路径映射到MEDIA_ROOT目录
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)