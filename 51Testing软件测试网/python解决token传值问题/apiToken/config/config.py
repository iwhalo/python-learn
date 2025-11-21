# config/config.py

# API 配置
HOST = "https://jsonplaceholder.typicode.com"  # 公开测试 API

# Token 配置
TOKEN_EXPIRE_TIME = 3600  # token 过期时间（秒）
REFRESH_TOKEN_BEFORE_EXPIRE = 300  # 提前刷新时间（秒）
MAX_RETRY_TIMES = 3  # 最大重试次数
RETRY_DELAY = 1  # 重试延迟（秒）

# 测试配置
TEST_PASSWORD = "123456789"
TEST_MOBILE = "13800000011"