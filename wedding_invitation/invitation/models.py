from django.db import models
from datetime import datetime
from django.conf import settings
from PIL import Image
import os


class WeddingEvent(models.Model):
    """
    婚礼事件模型，用于存储婚礼相关信息
    
    Attributes:
        title (CharField): 婚礼标题
        bride_name (CharField): 新娘姓名
        groom_name (CharField): 新郎姓名
        event_date (DateTimeField): 婚礼日期
        venue (CharField): 婚礼地点
        address (TextField): 详细地址
        description (TextField): 婚礼描述
        cover_image (ImageField): 封面图片
        created_at (DateTimeField): 创建时间
        updated_at (DateTimeField): 更新时间
    """
    title = models.CharField(max_length=200, verbose_name='婚礼标题')
    bride_name = models.CharField(max_length=100, verbose_name='新娘姓名')
    groom_name = models.CharField(max_length=100, verbose_name='新郎姓名')
    event_date = models.DateTimeField(verbose_name='婚礼日期')
    venue = models.CharField(max_length=300, verbose_name='婚礼地点')
    address = models.TextField(verbose_name='详细地址')
    description = models.TextField(blank=True, null=True, verbose_name='婚礼描述')
    cover_image = models.ImageField(upload_to=settings.WEDDING_COVERS_UPLOAD_PATH, blank=True, null=True, verbose_name='封面图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '婚礼活动'
        verbose_name_plural = '婚礼活动'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        重写save方法，在保存时处理封面图片
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"开始保存婚礼事件 - ID: {self.id}, 标题: {self.title}")
        super().save(*args, **kwargs)
        
        if self.cover_image:
            try:
                logger.info(f"开始处理封面图片 - 事件ID: {self.id}, 图片路径: {self.cover_image.path}")
                # 打开图片
                img = Image.open(self.cover_image.path)
                original_width, original_height = img.size
                logger.debug(f"原始图片尺寸 - 宽: {original_width}, 高: {original_height}")
                
                # 根据原始图片的比例决定使用哪种展示比例
                aspect_ratio = original_width / original_height
                logger.debug(f"图片宽高比: {aspect_ratio}")
                
                # 如果原始比例接近4:3或小于4:3，则使用4:3比例
                # 如果原始比例大于4:3（更宽），则使用9:16比例
                if aspect_ratio <= 1.5:  # 4:3 = 1.333..., 这里放宽到1.5
                    target_width = 800
                    target_height = 600  # 4:3比例
                    logger.debug(f"选择4:3比例 - 目标尺寸: {target_width}x{target_height}")
                else:  # 更宽的比例，使用9:16纵向比例
                    target_width = 600
                    target_height = 800  # 9:16比例
                    logger.debug(f"选择9:16比例 - 目标尺寸: {target_width}x{target_height}")
                
                # 根据目标尺寸裁剪图片
                img = self.crop_to_aspect_ratio_cover(img, target_width, target_height)
                
                # 保存处理后的图片
                img.save(self.cover_image.path, quality=85, optimize=True)
                logger.info(f"封面图片处理完成 - 事件ID: {self.id}, 保存路径: {self.cover_image.path}")
            except Exception as e:
                # 如果处理失败，不影响正常保存
                logger.error(f"封面图片处理失败 - 事件ID: {self.id}, 错误: {str(e)}")
                print(f"封面图片处理失败: {e}")
    
    def crop_to_aspect_ratio_cover(self, img, target_width, target_height):
        """
        将封面图片裁剪到指定的宽高比
        """
        original_width, original_height = img.size
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        
        if original_ratio > target_ratio:
            # 图片太宽，裁剪宽度
            new_width = int(original_height * target_ratio)
            offset = (original_width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, original_height))
        elif original_ratio < target_ratio:
            # 图片太高，裁剪高度
            new_height = int(original_width / target_ratio)
            offset = (original_height - new_height) // 2
            img = img.crop((0, offset, original_width, offset + new_height))
        # 如果比例相同，则无需裁剪
        
        # 调整到目标尺寸
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img
    



class Guest(models.Model):
    """
    宾客模型，用于记录参加婚礼的宾客信息
    
    Attributes:
        name (CharField): 宾客姓名
        phone (CharField): 联系电话
        email (EmailField): 邮箱
        invitation_code (CharField): 邀请码
        rsvp_status (BooleanField): 是否确认出席
        guest_count (PositiveIntegerField): 出席人数
        message (TextField): 祝福语
        created_at (DateTimeField): 创建时间
    """
    name = models.CharField(max_length=100, verbose_name='宾客姓名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    invitation_code = models.CharField(max_length=50, unique=True, verbose_name='邀请码')
    rsvp_status = models.BooleanField(default=False, verbose_name='是否确认出席')
    guest_count = models.PositiveIntegerField(default=1, verbose_name='出席人数')
    message = models.TextField(blank=True, verbose_name='祝福语')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '宾客'
        verbose_name_plural = '宾客'

    def __str__(self):
        return f"{self.name} ({self.invitation_code})"
    
    def is_attending(self):
        """
        判断宾客是否确认出席
        """
        return self.rsvp_status
    
    def get_total_guests_count(self):
        """
        获取该宾客带来的总人数
        """
        return self.guest_count if self.rsvp_status else 0


class GalleryImage(models.Model):
    """
    相册图片模型，用于展示婚礼相册
    
    Attributes:
        title (CharField): 图片标题
        image (ImageField): 图片文件
        description (TextField): 图片描述
        uploaded_at (DateTimeField): 上传时间
    """
    title = models.CharField(max_length=200, verbose_name='图片标题')
    image = models.ImageField(upload_to=settings.GALLERY_UPLOAD_PATH, verbose_name='图片')
    description = models.TextField(blank=True, null=True, verbose_name='图片描述')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '相册图片'
        verbose_name_plural = '相册图片'

    def __str__(self):
        return self.title

    def get_image_url(self):
        """
        安全获取图片URL的方法，如果图片不存在则返回None
        """
        if self.image and hasattr(self.image, 'url'):
            try:
                return self.image.url
            except ValueError:
                # 图片文件不存在
                return None
        return None

    def has_image(self):
        """
        检查是否有图片文件
        """
        return bool(self.get_image_url())
    
    def save(self, *args, **kwargs):
        """
        重写save方法，在保存时处理图片尺寸
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"开始保存相册图片 - ID: {self.id}, 标题: {self.title}")
        super().save(*args, **kwargs)
        
        if self.image:
            try:
                logger.info(f"开始处理相册图片 - 图片ID: {self.id}, 图片路径: {self.image.path}")
                # 打开图片
                img = Image.open(self.image.path)
                original_width, original_height = img.size
                logger.debug(f"原始图片尺寸 - 宽: {original_width}, 高: {original_height}")
                
                # 根据原始图片的比例决定使用哪种展示比例
                aspect_ratio = original_width / original_height
                logger.debug(f"图片宽高比: {aspect_ratio}")
                
                # 如果原始比例接近4:3或小于4:3，则使用4:3比例
                # 如果原始比例大于4:3（更宽），则使用9:16比例
                if aspect_ratio <= 1.5:  # 4:3 = 1.333..., 这里放宽到1.5
                    target_width = 800
                    target_height = 600  # 4:3比例
                    logger.debug(f"选择4:3比例 - 目标尺寸: {target_width}x{target_height}")
                else:  # 更宽的比例，使用9:16纵向比例
                    target_width = 600
                    target_height = 800  # 9:16比例（旋转后）
                    logger.debug(f"选择9:16比例 - 目标尺寸: {target_width}x{target_height}")
                
                # 根据目标尺寸裁剪图片
                img = self.crop_to_aspect_ratio(img, target_width, target_height)
                
                # 保存处理后的图片
                img.save(self.image.path, quality=85, optimize=True)
                logger.info(f"相册图片处理完成 - 图片ID: {self.id}, 保存路径: {self.image.path}")
            except Exception as e:
                # 如果处理失败，不影响正常保存
                logger.error(f"相册图片处理失败 - 图片ID: {self.id}, 错误: {str(e)}")
                print(f"图片处理失败: {e}")
    
    def crop_to_aspect_ratio(self, img, target_width, target_height):
        """
        将图片裁剪到指定的宽高比
        """
        original_width, original_height = img.size
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        
        if original_ratio > target_ratio:
            # 图片太宽，裁剪宽度
            new_width = int(original_height * target_ratio)
            offset = (original_width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, original_height))
        elif original_ratio < target_ratio:
            # 图片太高，裁剪高度
            new_height = int(original_width / target_ratio)
            offset = (original_height - new_height) // 2
            img = img.crop((0, offset, original_width, offset + new_height))
        # 如果比例相同，则无需裁剪
        
        # 调整到目标尺寸
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img


class PageVisit(models.Model):
    """
    页面访问统计模型
    
    Attributes:
        page_name (CharField): 页面名称
        visit_count (PositiveIntegerField): 访问次数
        last_visited (DateTimeField): 最后访问时间
    """
    page_name = models.CharField(max_length=100, verbose_name='页面名称')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='访问次数')
    last_visited = models.DateTimeField(auto_now=True, verbose_name='最后访问时间')
    
    class Meta:
        verbose_name = '页面访问统计'
        verbose_name_plural = '页面访问统计'
        unique_together = ('page_name',)  # 确保每个页面名称只有一条记录
    
    def __str__(self):
        return f'{self.page_name}: {self.visit_count} 次访问'
    
    @classmethod
    def increment_visit(cls, page_name):
        """
        增加页面访问次数
        
        Args:
            page_name (str): 页面名称
        
        Returns:
            PageVisit: 更新后的页面访问记录
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"增加页面访问次数 - 页面: {page_name}")
        
        visit_record, created = cls.objects.get_or_create(
            page_name=page_name,
            defaults={'visit_count': 1}
        )
        
        if not created:
            visit_record.visit_count += 1
            logger.debug(f"页面访问次数已更新 - 页面: {page_name}, 新次数: {visit_record.visit_count}")
        else:
            logger.debug(f"创建新的页面访问记录 - 页面: {page_name}, 初始次数: {visit_record.visit_count}")
        
        visit_record.save()
        logger.info(f"页面访问次数更新完成 - 页面: {page_name}, 总次数: {visit_record.visit_count}")
        
        return visit_record