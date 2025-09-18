import ssl
import certifi
import requests
from Demos.win32ts_logoff_disconnected import session

# 使用系统认证库
r=requests.get(url='https://example.com',verify=True)   # 默认

# 使用certifi认证库
r=requests.get('https://example.com',verify=certifi.where())

# 使用自定义认证文件
r=requests.get(url='https://example.com',verify='/path/to/ca-bundle.pem')

# 使用证书验证（不推荐）
r=requests.get('https://example.com',verify=False)

# 设置客户端证书
r=requests.get(url='https://example.com',cert=('/path/client.crt','/path/client.key'))

# 配置SSL上下文（高级用法）
import urllib3
https=urllib3.PoolManager(
    ssl_version=ssl.PROTOCOL_TLSv1_2, # 强制使用 TLS 1.2
    cert_reqs=ssl.CERT_REQUIRED, # 要求证书
    ca_certs=certifi.where(), # 证书包路径
    ciphers='HIGH:!DH:!anull'   # 自定义密码套件
)

# 自定义SSL配置的会话
session=requests.Session()
adapter=requests.adapters.HTTPAdapter(pool_connections=100,pool_maxsize=100)
session.mount('https://',adapter)
# urllib3 已在内部使用，可通过 HTTPAdapter 扩展配置
