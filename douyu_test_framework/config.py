"""测试框架配置文件"""
import os
from pydantic import BaseModel


class TestConfig(BaseModel):
    """测试配置设置"""
    base_url: str = "https://www.douyu.com"
    browser: str = "chromium"  # 浏览器类型: chromium, firefox, webkit
    headless: bool = False  # 是否无头模式
    slow_mo: int = 0  # 慢速执行延迟(毫秒)
    timeout: int = 30000  # 超时时间(毫秒)
    screenshot_on_failure: bool = True  # 失败时截图
    video_on_failure: bool = False  # 失败时录制视频
    

# 全局配置实例
config = TestConfig()
