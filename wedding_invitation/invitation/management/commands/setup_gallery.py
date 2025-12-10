from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = '设置相册图片目录并确保目录存在'

    def handle(self, *args, **options):
        # 创建相册和封面图片目录
        gallery_path = os.path.join(settings.MEDIA_ROOT, settings.GALLERY_UPLOAD_PATH)
        covers_path = os.path.join(settings.MEDIA_ROOT, settings.WEDDING_COVERS_UPLOAD_PATH)
        
        # 创建目录
        os.makedirs(gallery_path, exist_ok=True)
        os.makedirs(covers_path, exist_ok=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'成功创建相册目录: {gallery_path}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'成功创建封面图片目录: {covers_path}')
        )
        
        # 显示目录信息
        self.stdout.write(
            self.style.NOTICE(f'媒体文件根目录: {settings.MEDIA_ROOT}')
        )
        self.stdout.write(
            self.style.NOTICE(f'相册上传路径: {settings.GALLERY_UPLOAD_PATH}')
        )
        self.stdout.write(
            self.style.NOTICE(f'封面图片上传路径: {settings.WEDDING_COVERS_UPLOAD_PATH}')
        )