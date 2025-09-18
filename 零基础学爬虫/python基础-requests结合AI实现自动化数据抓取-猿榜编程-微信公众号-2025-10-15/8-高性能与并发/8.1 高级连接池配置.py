import requests
from urllib3 import PoolManager,Retry
import socket

# 创建自定义连接管理器
http=PoolManager(
    num_pools=50,       # 连接池数量
    maxsize=100,        # 每个连接池的最大连接数量
    block=False,        # 连接池满时不阻塞
    retries=Retry(3),   # 重试策略
    timeout=5.0,        # 超时设置
    socket_options=[
        (socket.IPPROTO_TCP,socket.TCP_NODELAY,1),      # 使用Nagle算法
        (socket.SOL_SOCKET,socket.SO_KEEPALIVE,1),      # 启用keepalive
        (socket.IPPROTO_TCP,socket.TCP_KEEPIDLE,60)     # keepalive空闲时间
    ]
)

# 将自定义连接管理器与Requests集成
session=requests.Session()
adapter=requests.adapters.HTTPAdapter(
    pool_connection=50,     # 连接池数量
    pool_maxsize=100,       # 每个连接池最大连接数
    max_retries=Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500,502,503,504]
    )
)
session.mount('http://',adapter)
session.mount('https://',adapter)