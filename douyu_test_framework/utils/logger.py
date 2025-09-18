"""框架的日志工具"""
import logging
import os
from datetime import datetime


class Logger:
    """测试框架的自定义日志记录器"""
    
    def __init__(self, name: str = "DouyuTestFramework"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 创建日志目录（如果不存在）
        os.makedirs("logs", exist_ok=True)
        
        # 文件处理器
        log_file = f"logs/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """记录调试消息"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """记录信息消息"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录警告消息"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录错误消息"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误消息"""
        self.logger.critical(message)


# 全局日志实例
logger = Logger()
