"""
创建PageVisit表的脚本
"""
import os
import sys
import django
from django.conf import settings

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_invitation.settings')
django.setup()

from django.db import connection

def create_pagevisit_table():
    """创建PageVisit表"""
    print("正在创建PageVisit表...")
    
    with connection.schema_editor() as schema_editor:
        from invitation.models import PageVisit
        schema_editor.create_model(PageVisit)
    
    print("PageVisit表创建完成！")
    
    # 初始化记录
    from invitation.models import PageVisit
    
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

if __name__ == "__main__":
    create_pagevisit_table()