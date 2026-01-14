"""
Django应用配置模块

这个模块定义了婚礼邀请函应用的配置信息，
包括应用名称、默认主键字段类型等。
"""

from django.apps import AppConfig


class InvitationConfig(AppConfig):
    """
    婚礼邀请函应用配置类
    
    这个类定义了invitation应用的基本配置信息，
    包括应用名称和默认的主键字段类型。
    
    Attributes:
        default_auto_field (str): 默认主键字段类型，使用BigAutoField
        name (str): 应用名称，对应Django项目中的app名称
    """
    default_auto_field = 'django.db.models.BigAutoField'  # 使用64位自增主键
    name = 'invitation'  # 应用名称，必须与项目结构中的文件夹名称一致