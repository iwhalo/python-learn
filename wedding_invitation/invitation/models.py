"""
婚礼邀请函应用的数据模型模块

这个模块定义了婚礼邀请函网站的所有数据模型，
包括婚礼事件、宾客信息、相册图片和页面访问统计。
每个模型都包含详细的字段定义、方法和文档字符串，
以及完整的日志记录功能。
"""

# 导入Django数据库模型基类 - 用于定义数据表结构
from django.db import models
# 导入Python内置日期时间模块 - 用于处理日期时间操作
from datetime import datetime
# 导入Django项目设置 - 用于访问配置参数
from django.conf import settings
# 导入Django时区工具 - 用于处理跨时区的时间操作
from django.utils import timezone
# 导入Python图像处理库 - 用于处理上传的图片文件
from PIL import Image
# 导入操作系统接口模块 - 用于处理文件路径等系统操作
import os


# 定义图片处理相关常量
# 相册图片标准尺寸比例 - 4:3横屏比例
STANDARD_GALLERY_RATIO_4_3 = (800, 600)
# 相册图片标准尺寸比例 - 9:16竖屏比例
STANDARD_GALLERY_RATIO_9_16 = (600, 800)
# 封面图片标准尺寸比例 - 4:3横屏比例
STANDARD_COVER_RATIO_4_3 = (800, 600)
# 封面图片标准尺寸比例 - 9:16竖屏比例
STANDARD_COVER_RATIO_9_16 = (600, 800)
# 图片处理质量百分比
IMAGE_PROCESSING_QUALITY = 85
# 默认缓存持续时间（小时）
DEFAULT_CACHE_DURATION_HOURS = 24 * 7  # 一周


class WeddingEvent(models.Model):
    """
    婚礼事件模型 - 存储婚礼的基本信息

    这个模型包含了婚礼的所有核心信息，包括新人姓名、
    婚礼日期、地点、描述和封面图片等。重写了save方法，
    实现了封面图片的自动裁剪和优化功能。

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
    # 婚礼标题，最大长度200字符
    title = models.CharField(max_length=200, verbose_name='婚礼标题')

    # 新娘姓名，最大长度100字符
    bride_name = models.CharField(max_length=100, verbose_name='新娘姓名')

    # 新郎姓名，最大长度100字符
    groom_name = models.CharField(max_length=100, verbose_name='新郎姓名')

    # 婚礼日期和时间
    event_date = models.DateTimeField(verbose_name='婚礼日期')

    # 婚礼举办地点，最大长度300字符
    venue = models.CharField(max_length=300, verbose_name='婚礼地点')

    # 婚礼详细地址，文本字段，无长度限制
    address = models.TextField(verbose_name='详细地址')

    # 婚礼描述，可选字段，可以为空
    description = models.TextField(blank=True, null=True, verbose_name='婚礼描述')

    # 封面图片，上传到WEDDING_COVERS_UPLOAD_PATH目录，可选字段
    cover_image = models.ImageField(
        upload_to=settings.WEDDING_COVERS_UPLOAD_PATH,
        blank=True,
        null=True,
        verbose_name='封面图片'
    )

    # 创建时间，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 更新时间，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 模型元数据配置
    class Meta:
        verbose_name = '婚礼活动'  # 单数形式的模型名称
        verbose_name_plural = '婚礼活动'  # 复数形式的模型名称

    def __str__(self):
        """返回婚礼标题作为字符串表示"""
        return self.title

    def save(self, *args, **kwargs):
        """
        重写save方法，在保存时自动处理封面图片

        功能：
        - 根据图片原始比例选择合适的裁剪比例
        - 将图片裁剪为标准比例（4:3或9:16）
        - 优化图片质量和尺寸

        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        """
        import logging
        logger = logging.getLogger(__name__)

        # 记录开始保存婚礼事件
        logger.info(f"开始保存婚礼事件 - ID: {self.id}, 标题: {self.title}")

        # 先调用父类的save方法保存基础信息
        super().save(*args, **kwargs)

        # 如果有封面图片，则进行处理
        if self.cover_image:
            try:
                # 记录开始处理封面图片
                logger.info(f"开始处理封面图片 - 事件ID: {self.id}, 图片路径: {self.cover_image.path}")

                # 打开图片文件
                img = Image.open(self.cover_image.path)
                original_width, original_height = img.size
                logger.debug(f"原始图片尺寸 - 宽: {original_width}, 高: {original_height}")

                # 计算图片的宽高比
                aspect_ratio = original_width / original_height
                logger.debug(f"图片宽高比: {aspect_ratio}")

                # 根据原始图片的比例决定使用哪种展示比例
                # 如果原始比例接近4:3或小于4:3，则使用4:3比例
                # 如果原始比例大于4:3（更宽），则使用9:16比例
                if aspect_ratio <= 1.5:  # 4:3 = 1.333..., 这里放宽到1.5
                    target_width, target_height = STANDARD_COVER_RATIO_4_3  # 4:3比例
                    logger.debug(f"选择4:3比例 - 目标尺寸: {target_width}x{target_height}")
                else:  # 更宽的比例，使用9:16纵向比例
                    target_width, target_height = STANDARD_COVER_RATIO_9_16  # 9:16比例
                    logger.debug(f"选择9:16比例 - 目标尺寸: {target_width}x{target_height}")

                # 根据目标尺寸裁剪图片
                img = self.crop_to_aspect_ratio_cover(img, target_width, target_height)

                # 保存处理后的图片，使用预设的质量参数，启用优化
                img.save(self.cover_image.path, quality=IMAGE_PROCESSING_QUALITY, optimize=True)
                logger.info(f"封面图片处理完成 - 事件ID: {self.id}, 保存路径: {self.cover_image.path}")
            except Exception as e:
                # 如果处理失败，记录错误但不影响正常保存
                logger.error(f"封面图片处理失败 - 事件ID: {self.id}, 错误: {str(e)}")
                print(f"封面图片处理失败: {e}")

    def crop_to_aspect_ratio_cover(self, img, target_width, target_height):
        """
        将封面图片裁剪到指定的宽高比

        使用智能裁剪算法，保持图片的主要内容区域，
        确保在不同设备上都有良好的显示效果。

        Args:
            img: PIL Image对象
            target_width: 目标宽度
            target_height: 目标高度

        Returns:
            PIL Image对象: 裁剪后的图片
        """
        # 获取原始图片尺寸
        original_width, original_height = img.size

        # 计算目标宽高比和原始宽高比
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height

        if original_ratio > target_ratio:
            # 图片太宽，裁剪宽度（从中间裁剪）
            new_width = int(original_height * target_ratio)
            offset = (original_width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, original_height))
        elif original_ratio < target_ratio:
            # 图片太高，裁剪高度（从中间裁剪）
            new_height = int(original_width / target_ratio)
            offset = (original_height - new_height) // 2
            img = img.crop((0, offset, original_width, offset + new_height))
        # 如果比例相同，则无需裁剪

        # 调整到目标尺寸，使用LANCZOS重采样算法以获得最佳质量
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img


class Guest(models.Model):
    """
    宾客模型，用于记录参加婚礼的宾客信息

    这个模型存储了宾客的基本信息和RSVP状态，
    包括姓名、联系方式、邀请码、是否确认出席等信息。

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
    # 宾客姓名，最大长度100字符
    name = models.CharField(max_length=100, verbose_name='宾客姓名')

    # 联系电话，最大长度20字符，可选字段
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')

    # 邮箱地址，可选字段
    email = models.EmailField(blank=True, verbose_name='邮箱')

    # 邀请码，最大长度50字符，唯一字段
    invitation_code = models.CharField(max_length=50, unique=True, verbose_name='邀请码')

    # RSVP状态，默认为False（未确认）
    rsvp_status = models.BooleanField(default=False, verbose_name='是否确认出席')

    # 出席人数，默认为1，必须为正整数
    guest_count = models.PositiveIntegerField(default=1, verbose_name='出席人数')

    # 祝福语，可选字段
    message = models.TextField(blank=True, verbose_name='祝福语')

    # 创建时间，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 模型元数据配置
    class Meta:
        verbose_name = '宾客'  # 单数形式的模型名称
        verbose_name_plural = '宾客'  # 复数形式的模型名称

    def __str__(self):
        """返回宾客姓名和邀请码作为字符串表示"""
        return f"{self.name} ({self.invitation_code})"

    def is_attending(self):
        """
        判断宾客是否确认出席

        Returns:
            bool: 如果宾客确认出席返回True，否则返回False
        """
        return self.rsvp_status

    def get_total_guests_count(self):
        """
        获取该宾客带来的总人数

        Returns:
            int: 如果宾客确认出席返回出席人数，否则返回0
        """
        return self.guest_count if self.rsvp_status else 0


class GalleryImage(models.Model):
    """
    相册图片模型，用于展示婚礼相册

    这个模型存储了婚礼相册中的图片信息，
    包括图片标题、图片文件、描述等。
    重写了save方法，实现了图片的自动裁剪和优化功能。

    Attributes:
        title (CharField): 图片标题
        image (ImageField): 图片文件
        description (TextField): 图片描述
        uploaded_at (DateTimeField): 上传时间
    """
    # 图片标题，最大长度200字符
    title = models.CharField(max_length=200, verbose_name='图片标题')

    # 图片文件，上传到GALLERY_UPLOAD_PATH目录
    image = models.ImageField(upload_to=settings.GALLERY_UPLOAD_PATH, verbose_name='图片')

    # 图片描述，可选字段
    description = models.TextField(blank=True, null=True, verbose_name='图片描述')

    # 上传时间，自动添加当前时间
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    # 模型元数据配置
    class Meta:
        verbose_name = '相册图片'  # 单数形式的模型名称
        verbose_name_plural = '相册图片'  # 复数形式的模型名称

    def __str__(self):
        """返回图片标题作为字符串表示"""
        return self.title

    def get_image_url(self):
        """
        安全获取图片URL的方法，如果图片不存在则返回None

        Returns:
            str: 图片URL，如果图片不存在则返回None
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

        Returns:
            bool: 如果有图片文件返回True，否则返回False
        """
        return bool(self.get_image_url())

    def save(self, *args, **kwargs):
        """
        重写save方法，在保存时处理图片尺寸

        功能：
        - 根据图片原始比例选择合适的裁剪比例
        - 将图片裁剪为标准比例（4:3或9:16）
        - 优化图片质量和尺寸

        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        """
        import logging
        logger = logging.getLogger(__name__)

        # 记录开始保存相册图片
        logger.info(f"开始保存相册图片 - ID: {self.id}, 标题: {self.title}")

        # 先调用父类的save方法保存基础信息
        super().save(*args, **kwargs)

        # 如果有图片，则进行处理
        if self.image:
            try:
                # 记录开始处理相册图片
                logger.info(f"开始处理相册图片 - 图片ID: {self.id}, 图片路径: {self.image.path}")

                # 打开图片文件
                img = Image.open(self.image.path)
                original_width, original_height = img.size
                logger.debug(f"原始图片尺寸 - 宽: {original_width}, 高: {original_height}")

                # 计算图片的宽高比
                aspect_ratio = original_width / original_height
                logger.debug(f"图片宽高比: {aspect_ratio}")

                # 根据原始图片的比例决定使用哪种展示比例
                # 如果原始比例接近4:3或小于4:3，则使用4:3比例
                # 如果原始比例大于4:3（更宽），则使用9:16比例
                if aspect_ratio <= 1.5:  # 4:3 = 1.333..., 这里放宽到1.5
                    target_width, target_height = STANDARD_GALLERY_RATIO_4_3  # 4:3比例
                    logger.debug(f"选择4:3比例 - 目标尺寸: {target_width}x{target_height}")
                else:  # 更宽的比例，使用9:16纵向比例
                    target_width, target_height = STANDARD_GALLERY_RATIO_9_16  # 9:16比例（旋转后）
                    logger.debug(f"选择9:16比例 - 目标尺寸: {target_width}x{target_height}")

                # 根据目标尺寸裁剪图片
                img = self.crop_to_aspect_ratio(img, target_width, target_height)

                # 保存处理后的图片，使用预设的质量参数，启用优化
                img.save(self.image.path, quality=IMAGE_PROCESSING_QUALITY, optimize=True)
                logger.info(f"相册图片处理完成 - 图片ID: {self.id}, 保存路径: {self.image.path}")
            except Exception as e:
                # 如果处理失败，记录错误但不影响正常保存
                logger.error(f"相册图片处理失败 - 图片ID: {self.id}, 错误: {str(e)}")
                print(f"图片处理失败: {e}")

    def crop_to_aspect_ratio(self, img, target_width, target_height):
        """
        将图片裁剪到指定的宽高比

        使用智能裁剪算法，保持图片的主要内容区域，
        确保在不同设备上都有良好的显示效果。

        Args:
            img: PIL Image对象
            target_width: 目标宽度
            target_height: 目标高度

        Returns:
            PIL Image对象: 裁剪后的图片
        """
        # 获取原始图片尺寸
        original_width, original_height = img.size

        # 计算目标宽高比和原始宽高比
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height

        if original_ratio > target_ratio:
            # 图片太宽，裁剪宽度（从中间裁剪）
            new_width = int(original_height * target_ratio)
            offset = (original_width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, original_height))
        elif original_ratio < target_ratio:
            # 图片太高，裁剪高度（从中间裁剪）
            new_height = int(original_width / target_ratio)
            offset = (original_height - new_height) // 2
            img = img.crop((0, offset, original_width, offset + new_height))
        # 如果比例相同，则无需裁剪

        # 调整到目标尺寸，使用LANCZOS重采样算法以获得最佳质量
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img


class PageVisit(models.Model):
    """
    页面访问统计模型

    这个模型用于统计网站各页面的访问次数，
    可以帮助分析网站的访问情况和用户行为。

    Attributes:
        page_name (CharField): 页面名称
        visit_count (PositiveIntegerField): 访问次数
        last_visited (DateTimeField): 最后访问时间
    """
    # 页面名称，最大长度100字符
    page_name = models.CharField(max_length=100, verbose_name='页面名称')

    # 访问次数，默认为0，必须为正整数
    visit_count = models.PositiveIntegerField(default=0, verbose_name='访问次数')

    # 最后访问时间，自动更新为当前时间
    last_visited = models.DateTimeField(auto_now=True, verbose_name='最后访问时间')

    def __str__(self):
        """返回页面名称和访问次数作为字符串表示"""
        return f'{self.page_name}: {self.visit_count} 次访问'

    @classmethod
    def increment_visit(cls, page_name):
        """
        增加页面访问次数的类方法

        这个方法用于记录页面访问，如果页面记录不存在则创建新记录，
        如果存在则增加访问次数。所有操作都有详细的日志记录。

        Args:
            page_name (str): 页面名称

        Returns:
            PageVisit: 更新后的页面访问记录
        """
        import logging
        logger = logging.getLogger(__name__)

        # 记录开始增加页面访问次数
        logger.info(f"增加页面访问次数 - 页面: {page_name}")

        # 尝试获取或创建页面访问记录
        visit_record, created = cls.objects.get_or_create(
            page_name=page_name,
            defaults={'visit_count': 1}
        )

        if not created:
            # 如果记录已存在，增加访问次数
            visit_record.visit_count += 1
            logger.debug(f"页面访问次数已更新 - 页面: {page_name}, 新次数: {visit_record.visit_count}")
        else:
            # 如果是新创建的记录，记录初始次数
            logger.debug(f"创建新的页面访问记录 - 页面: {page_name}, 初始次数: {visit_record.visit_count}")

        # 保存记录
        visit_record.save()
        logger.info(f"页面访问次数更新完成 - 页面: {page_name}, 总次数: {visit_record.visit_count}")
        
        return visit_record

    # 模型元数据配置
    class Meta:
        verbose_name = '页面访问统计'  # 单数形式的模型名称
        verbose_name_plural = '页面访问统计'  # 复数形式的模型名称
        unique_together = ('page_name',)  # 确保每个页面名称只有一条记录


class GeocodingCache(models.Model):
    """
    地理编码缓存模型 - 存储地理编码查询结果以避免重复API调用

    这个模型用于缓存高德地图API的地理编码结果，提高性能并减少API调用次数。
    当相同的地址被多次查询时，可以直接从缓存中获取结果。

    Attributes:
        address (TextField): 查询的地址
        latitude (DecimalField): 纬度
        longitude (DecimalField): 经度
        result_data (JSONField): 完整的地理编码结果数据
        created_at (DateTimeField): 缓存创建时间
        updated_at (DateTimeField): 缓存更新时间
        expires_at (DateTimeField): 缓存过期时间
    """
    address = models.TextField(verbose_name='查询地址')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, verbose_name='经度')
    result_data = models.JSONField(verbose_name='地理编码结果数据', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    expires_at = models.DateTimeField(verbose_name='过期时间')

    class Meta:
        verbose_name = '地理编码缓存'
        verbose_name_plural = '地理编码缓存'
        indexes = [
            models.Index(fields=['address']),  # 为地址字段创建索引以提高查询效率
            models.Index(fields=['expires_at']),  # 为过期时间创建索引以提高清理效率
        ]
        unique_together = ('address',)  # 确保每个地址只有一条缓存记录

    def __str__(self):
        return f'{self.address} -> ({self.latitude}, {self.longitude})'

    @classmethod
    def get_cached_result(cls, address):
        """
        根据地址获取缓存的地理编码结果

        Args:
            address (str): 要查询的地址

        Returns:
            dict or None: 如果缓存存在且未过期，返回地理编码结果；否则返回None
        """
        try:
            cache_entry = cls.objects.get(address=address)
            if cache_entry.expires_at > timezone.now():
                # 缓存未过期，返回缓存结果
                return cache_entry.result_data
            else:
                # 缓存已过期，删除它
                cache_entry.delete()
                return None
        except cls.DoesNotExist:
            # 没有找到缓存
            return None

    @classmethod
    def set_cache_result(cls, address, geocoding_result, cache_duration_hours=DEFAULT_CACHE_DURATION_HOURS):  # 默认缓存一周
        """
        将地理编码结果存入缓存

        Args:
            address (str): 查询的地址
            geocoding_result (dict): 地理编码结果
            cache_duration_hours (int): 缓存持续时间（小时）
        """
        from django.utils import timezone
        from datetime import timedelta
        
        # 计算过期时间
        expires_at = timezone.now() + timedelta(hours=cache_duration_hours)
        
        # 创建或更新缓存条目
        cls.objects.update_or_create(
            address=address,
            defaults={
                'latitude': geocoding_result['latitude'],
                'longitude': geocoding_result['longitude'],
                'result_data': geocoding_result,
                'expires_at': expires_at
            }
        )

    @classmethod
    def cleanup_expired_cache(cls):
        """
        清理过期的缓存条目

        Returns:
            int: 删除的条目数量
        """
        from django.utils import timezone
        expired_entries = cls.objects.filter(expires_at__lt=timezone.now())
        count = expired_entries.count()
        expired_entries.delete()
        return count


class APIUsageStats(models.Model):
    """
    API使用统计模型 - 记录高德地图API调用统计信息

    用于跟踪API调用频率，帮助管理API限制和配额。

    Attributes:
        api_type (CharField): API类型（geocode或reverse_geocode）
        date (DateField): 统计日期
        call_count (IntegerField): 当日调用次数
        success_count (IntegerField): 成功调用次数
        error_count (IntegerField): 错误调用次数
        rate_limit_hit (BooleanField): 是否达到速率限制
        created_at (DateTimeField): 创建时间
        updated_at (DateTimeField): 更新时间
    """
    API_TYPES = [
        ('geocode', '地理编码'),
        ('reverse_geocode', '逆地理编码'),
    ]
    
    api_type = models.CharField(max_length=20, choices=API_TYPES, verbose_name='API类型')
    date = models.DateField(verbose_name='统计日期')
    call_count = models.IntegerField(default=0, verbose_name='调用次数')
    success_count = models.IntegerField(default=0, verbose_name='成功次数')
    error_count = models.IntegerField(default=0, verbose_name='错误次数')
    rate_limit_hit = models.BooleanField(default=False, verbose_name='达到速率限制')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'API使用统计'
        verbose_name_plural = 'API使用统计'
        unique_together = ('api_type', 'date')  # 确保每种API类型每天只有一条统计记录
        indexes = [
            models.Index(fields=['api_type', 'date']),  # 为API类型和日期创建复合索引
        ]

    def __str__(self):
        return f'{self.api_type} - {self.date} ({self.call_count}次调用)'

    @classmethod
    def increment_call(cls, api_type, success=True):
        """
        增加API调用统计

        Args:
            api_type (str): API类型
            success (bool): 调用是否成功
        """
        from django.utils import timezone
        from django.db import transaction
        
        today = timezone.now().date()
        
        with transaction.atomic():
            stat, created = cls.objects.select_for_update().get_or_create(
                api_type=api_type,
                date=today,
                defaults={'call_count': 0, 'success_count': 0, 'error_count': 0}
            )
            
            stat.call_count += 1
            if success:
                stat.success_count += 1
            else:
                stat.error_count += 1
            
            stat.save(update_fields=['call_count', 'success_count', 'error_count', 'updated_at'])

    @classmethod
    def check_rate_limit(cls, api_type, daily_limit=1000):
        """
        检查是否达到每日调用限制

        Args:
            api_type (str): API类型
            daily_limit (int): 每日调用限制

        Returns:
            bool: True表示未超过限制，False表示已超过限制
        """
        from django.utils import timezone
        today = timezone.now().date()
        
        try:
            stat = cls.objects.get(api_type=api_type, date=today)
            return stat.call_count < daily_limit
        except cls.DoesNotExist:
            return True  # 如果没有统计记录，认为未超过限制

    @classmethod
    def get_daily_stats(cls, api_type, date):
        """
        获取指定日期的API调用统计

        Args:
            api_type (str): API类型
            date (datetime.date): 日期

        Returns:
            APIUsageStats or None: 统计记录，如果不存在则返回None
        """
        try:
            return cls.objects.get(api_type=api_type, date=date)
        except cls.DoesNotExist:
            return None