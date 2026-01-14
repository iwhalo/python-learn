"""
Django管理命令：设置相册图片目录

这个命令用于创建婚礼邀请函系统所需的媒体文件目录，
确保相册图片和婚礼封面图片有合适的存储位置。
可以通过 `python manage.py setup_gallery` 命令调用。
"""

import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

# 获取logger实例，用于记录日志
logger = logging.getLogger('invitation')


class Command(BaseCommand):
    """
    设置相册图片目录的Django管理命令

    这个命令会创建两个目录：
    1. 相册图片目录 - 用于存储用户上传的婚礼照片
    2. 婚礼封面图片目录 - 用于存储婚礼事件的封面图片

    使用方法:
        python manage.py setup_gallery
    """

    # 命令的帮助信息，当用户执行 `python manage.py help setup_gallery` 时显示
    help = '设置相册图片目录并确保目录存在'

    def handle(self, *args, **options):
        """
        执行命令的主要逻辑

        这个方法会：
        1. 构建相册和封面图片的完整路径
        2. 创建这些目录（如果不存在）
        3. 输出操作结果和配置信息
        """
        # 构建相册图片目录的完整路径
        # settings.MEDIA_ROOT 是媒体文件的根目录
        # settings.GALLERY_UPLOAD_PATH 是相册图片的相对路径
        gallery_path = os.path.join(settings.MEDIA_ROOT, settings.GALLERY_UPLOAD_PATH)

        # 构建婚礼封面图片目录的完整路径
        # settings.WEDDING_COVERS_UPLOAD_PATH 是封面图片的相对路径
        covers_path = os.path.join(settings.MEDIA_ROOT, settings.WEDDING_COVERS_UPLOAD_PATH)

        # 记录开始创建目录的日志
        logger.info(f"开始创建相册目录 - 相册路径: {gallery_path}, 封面路径: {covers_path}")

        # 创建相册图片目录
        # exist_ok=True 表示如果目录已存在，不会抛出异常
        os.makedirs(gallery_path, exist_ok=True)

        # 创建婚礼封面图片目录
        os.makedirs(covers_path, exist_ok=True)

        # 记录目录创建成功的日志
        logger.info("相册目录创建完成")

        # 输出成功信息到控制台
        self.stdout.write(
            self.style.SUCCESS(f'成功创建相册目录: {gallery_path}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'成功创建封面图片目录: {covers_path}')
        )

        # 显示配置信息，帮助用户了解目录结构
        self.stdout.write(
            self.style.NOTICE(f'媒体文件根目录: {settings.MEDIA_ROOT}')
        )
        self.stdout.write(
            self.style.NOTICE(f'相册上传路径: {settings.GALLERY_UPLOAD_PATH}')
        )
        self.stdout.write(
            self.style.NOTICE(f'封面图片上传路径: {settings.WEDDING_COVERS_UPLOAD_PATH}')
        )