"""
执行数据库迁移的脚本
"""
import os
import sys
import django
from django.conf import settings

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_invitation.settings')
django.setup()

def run_migrations():
    """运行数据库迁移"""
    print("正在执行数据库迁移...")
    
    # 导入Django迁移相关模块
    from django.core.management import execute_from_command_line
    import subprocess
    
    try:
        # 尝试使用subprocess运行迁移命令
        result = subprocess.run([
            sys.executable, 
            'manage.py', 
            'makemigrations'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("创建迁移文件成功:")
            print(result.stdout)
        else:
            print("创建迁移文件失败:")
            print(result.stderr)
        
        # 再次尝试运行migrate命令
        result = subprocess.run([
            sys.executable, 
            'manage.py', 
            'migrate'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("\n数据库迁移成功:")
            print(result.stdout)
        else:
            print("\n数据库迁移失败:")
            print(result.stderr)
            
    except Exception as e:
        print(f"执行迁移时出错: {e}")
        
        # 如果subprocess不行，尝试直接使用Django API
        try:
            print("尝试使用Django迁移API...")
            from django.core.management.sql import sql_migrate
            from django.db import connections
            from django.db.migrations.executor import MigrationExecutor
            
            # 这种方式比较复杂，我们可以直接创建表
            create_tables_directly()
            
        except Exception as e2:
            print(f"Django API方式也失败: {e2}")

def create_tables_directly():
    """直接创建所需的数据库表"""
    print("尝试直接创建数据库表...")
    
    from django.db import connection
    from invitation.models import PageVisit
    
    # 检查表是否已存在
    table_exists = PageVisit._meta.db_table in connection.introspection.table_names()
    
    if not table_exists:
        print(f"创建 {PageVisit._meta.db_table} 表...")
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(PageVisit)
        print("表创建成功!")
    else:
        print(f"表 {PageVisit._meta.db_table} 已存在")
    
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
    run_migrations()