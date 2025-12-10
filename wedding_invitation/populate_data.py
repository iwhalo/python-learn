"""
婚礼邀请系统数据填充脚本
用于初始化演示数据
"""

import os
import sys
import django
from datetime import datetime, timedelta

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_invitation.settings')
django.setup()

from invitation.models import WeddingEvent, Guest, GalleryImage


def populate_wedding_data():
    """填充婚礼相关数据"""
    print("开始填充婚礼数据...")
    
    # 创建婚礼事件
    wedding_event, created = WeddingEvent.objects.get_or_create(
        title="张三 & 李四的婚礼",
        defaults={
            'bride_name': '李四',
            'groom_name': '张三',
            'event_date': datetime.now() + timedelta(days=30),  # 30天后的婚礼
            'venue': '北京香格里拉大酒店',
            'address': '北京市朝阳区东三环北路29号',
            'description': '诚邀各位亲朋好友共同见证我们的幸福时刻，分享这份喜悦与美好。'
        }
    )
    
    if created:
        print(f"创建婚礼事件: {wedding_event.title}")
    else:
        print(f"婚礼事件已存在: {wedding_event.title}")
    
    # 创建一些宾客
    guests_data = [
        {'name': '王五', 'phone': '13800138000', 'email': 'wangwu@example.com', 'invitation_code': 'GUEST001'},
        {'name': '赵六', 'phone': '13800138001', 'email': 'zhaoliu@example.com', 'invitation_code': 'GUEST002'},
        {'name': '孙七', 'phone': '13800138002', 'email': 'sunqi@example.com', 'invitation_code': 'GUEST003'},
    ]
    
    for guest_data in guests_data:
        guest, created = Guest.objects.get_or_create(
            invitation_code=guest_data['invitation_code'],
            defaults=guest_data
        )
        if created:
            print(f"创建宾客: {guest.name}")
        else:
            print(f"宾客已存在: {guest.name}")
    
    # 创建一些相册图片
    images_data = [
        {
            'title': '订婚照',
            'description': '我们的订婚照片，记录下这美好的时刻'
        },
        {
            'title': '婚纱照',
            'description': '精心拍摄的婚纱照，每一帧都是爱的见证'
        },
        {
            'title': '旅行照',
            'description': '一起走过的风景，见证我们的爱情历程'
        },
        {
            'title': '情侣照',
            'description': '日常生活中的甜蜜瞬间'
        },
        {
            'title': '婚礼彩排',
            'description': '婚礼前的彩排，紧张而兴奋'
        },
        {
            'title': '亲友聚会',
            'description': '与亲朋好友共度的美好时光'
        },
    ]
    
    for idx, img_data in enumerate(images_data, 1):
        # 在演示中，我们只创建记录而不实际上传图片
        # 实际部署时需要上传真实的图片文件
        gallery_img, created = GalleryImage.objects.get_or_create(
            title=img_data['title'],
            defaults={
                'description': img_data['description']
            }
        )
        if created:
            print(f"创建相册图片: {gallery_img.title}")
        else:
            print(f"相册图片已存在: {gallery_img.title}")
    
    print("数据填充完成！")


if __name__ == "__main__":
    populate_wedding_data()