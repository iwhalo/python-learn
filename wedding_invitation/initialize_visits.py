"""
初始化访问统计数据的脚本
"""
import os
import sys
import django
from django.conf import settings

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_invitation.settings')
django.setup()

def initialize_page_visits():
    """初始化页面访问统计"""
    print("初始化页面访问统计数据...")
    
    from invitation.models import PageVisit
    from django.db import connection
    
    try:
        # 检查表是否已存在
        table_names = connection.introspection.table_names()
        table_exists = PageVisit._meta.db_table in table_names
        
        if not table_exists:
            print(f"表 {PageVisit._meta.db_table} 不存在，需要先运行迁移命令")
            print("请运行: python manage.py migrate")
            return
        else:
            print(f"表 {PageVisit._meta.db_table} 已存在")
        
        # 创建首页访问记录
        homepage_record, created = PageVisit.objects.get_or_create(
            page_name='homepage',
            defaults={'visit_count': 0}
        )
        if created:
            print("创建首页访问记录")
        else:
            print(f"首页已有访问记录，当前访问次数: {homepage_record.visit_count}")

        # 创建宾客列表页面访问记录
        guest_list_record, created = PageVisit.objects.get_or_create(
            page_name='guest_list_page',
            defaults={'visit_count': 0}
        )
        if created:
            print("创建宾客列表页面访问记录")
        else:
            print(f"宾客列表页面已有访问记录，当前访问次数: {guest_list_record.visit_count}")

        print("页面访问统计初始化完成！")

    except Exception as e:
        print(f"初始化页面访问统计时出错: {e}")
        print("可能需要先运行数据库迁移命令: python manage.py migrate")


if __name__ == "__main__":
    initialize_page_visits()