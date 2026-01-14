# 高德地图API密钥配置指南

## 1. 申请API密钥

1. 访问高德开放平台：https://lbs.amap.com/
2. 注册开发者账号并登录
3. 进入「控制台」-「应用管理」-「创建新应用」
4. 应用平台选择「Web端(JSAPI)」
5. 在「服务类型」中勾选「JavaScript API」和「Web服务API」
6. 获取API Key和安全密钥(jscode)

### 重要提醒
- **务必同时勾选JavaScript API和Web服务API**，因为项目同时使用这两种服务
- **安全密钥(jscode)** 是2021年12月2日后申请的API Key必需的配置
- 请记录好API Key和安全密钥，后续配置中都需要使用

## 2. 配置API密钥

### 方法一：环境变量配置（推荐）

**创建`.env`文件**：复制`.env.example`文件为`.env`，然后填入API密钥：
```bash
# 高德地图API密钥
AMAP_API_KEY=您申请的API密钥
AMAP_SECURITY_JS_CODE=您申请的安全密钥

# Django设置
DEBUG=True
SECRET_KEY=您的Django密钥
```

**在settings.py中读取环境变量**：
```python
import os
from pathlib import Path

# 高德地图API密钥
AMAP_WEB_SERVICE_KEY = os.environ.get('AMAP_WEB_SERVICE_KEY', '')  # 从环境变量获取Web服务API密钥
AMAP_JS_API_KEY = os.environ.get('AMAP_JS_API_KEY', '')  # 从环境变量获取JavaScript API密钥
AMAP_SECURITY_JS_CODE = os.environ.get('AMAP_SECURITY_JS_CODE', '')  # 安全密钥
```

### 方法二：直接修改settings.py

编辑 `wedding_invitation/settings.py` 文件：

```python
import os

# 高德地图API密钥
# 用于地理编码和地图展示功能
AMAP_API_KEY = '您的API密钥'  # 直接配置API密钥

# 高德地图安全密钥（必需，用于JS API 2.0）
AMAP_SECURITY_JS_CODE = '您的安全密钥'  # 安全密钥，强烈建议配置
```

## 3. 安全密钥配置方式

### 方式一：后端传递安全密钥（推荐，项目已预配置）

项目已配置从后端传递安全密钥到前端，这是最安全的方式，无需手动修改HTML文件：

**在views.py中**：
```python
from django.conf import settings

context = {
    'amap_api_key': settings.AMAP_API_KEY,
    'amap_security_js_code': settings.AMAP_SECURITY_JS_CODE,
    # 其他上下文数据
}
```

**在模板中**：
```html
<script type="text/javascript">
    window._AMapSecurityConfig = {
        securityJsCode: '{{ amap_security_js_code|default:"" }}',
    };
</script>
```

### 方式二：代理服务器配置（生产环境最佳实践）

在生产环境中，最安全的方式是使用反向代理隐藏安全密钥：

**Nginx配置示例**：
```nginx
server {
    listen       80;
    server_name  your-domain.com;  # 替换为你的域名

    # 高德地图服务代理
    location /_AMapService/ {
        rewrite ^/_AMapService/(.*)$ /$1 break;
        proxy_pass https://webapi.amap.com;
        proxy_set_header Host webapi.amap.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # 在这里添加安全密钥参数
        proxy_set_header X-Amz-Cf-Pop $http_x_amz_cf_pop;
    }
    
    # Web服务API代理
    location /_AMapAPI/ {
        rewrite ^/_AMapAPI/(.*)$ /$1?key=您的API_KEY&jscode=您的安全密钥&$args break;
        proxy_pass https://restapi.amap.com;
        proxy_set_header Host restapi.amap.com;
    }
}
```

**前端配置**：
```javascript
window._AMapSecurityConfig = {
    serviceHost: '//your-domain.com/_AMapService',  // 代理服务器地址
};
```

### 方式三：静态安全密钥配置（开发环境临时使用）

仅在开发环境中临时使用，**生产环境不推荐**：

```javascript
window._AMapSecurityConfig = {
    securityJsCode: '您的安全密钥', // 请替换为你的安全密钥
}
```

## 4. 配置验证

### 验证API密钥
1. 启动项目：`python manage.py runserver`
2. 访问地图页面：`http://127.0.0.1:8000/map/`
3. 打开浏览器开发者工具，查看Console是否有错误信息

### 验证安全密钥
1. 查看Network标签页，确认地图相关资源加载成功
2. 地图应能正常显示，包含道路名称、建筑物名称等详细信息
3. 检查是否有类似`INVALID_SECURITY_CODE`的错误

### 使用管理命令验证
```bash
# 查看API使用统计
python manage.py show_api_stats

# 检查地理编码功能
python manage.py shell
>>> from invitation.views import geocode_address
>>> from django.conf import settings
>>> result = geocode_address(address="北京市天安门", api_key=settings.AMAP_API_KEY)
>>> print(result)
```

## 5. 最佳实践

### 开发环境配置
- 使用环境变量管理API密钥
- 将`.env`文件加入`.gitignore`，避免提交到代码仓库
- 使用不同的API密钥区分开发和生产环境

### 生产环境配置
- **务必使用代理服务器方式**隐藏安全密钥
- 定期检查API使用统计，避免超出调用限制
- 使用HTTPS协议确保通信安全
- 配置API密钥的IP白名单（如果可用）

### 安全建议
- **绝不在代码中硬编码API密钥**
- **绝不在公共仓库中暴露API密钥**
- **定期轮换API密钥**
- **监控API调用统计**
- **使用最小权限原则配置API密钥**

## 6. 常见问题排查

### API密钥无效
- **错误信息**：`INVALID_USER_KEY`
- **解决方法**：检查API密钥是否正确，确认申请时选择了正确的服务类型

### 安全密钥错误
- **错误信息**：`INVALID_SECURITY_CODE` 或 `JSAPI_LOAD_ERROR`
- **解决方法**：检查安全密钥是否正确，确认配置方式是否正确

### API调用超限
- **错误信息**：`OVER_LIMIT`
- **解决方法**：检查API调用统计，考虑升级API套餐或优化调用频率

### 地图加载失败
- **可能原因**：域名未在高德平台配置、安全密钥配置错误
- **解决方法**：确认域名已在高德平台配置，检查安全密钥配置

## 7. 注意事项

- 2021年12月2日之后申请的API Key必须配合安全密钥使用
- API密钥请勿在公共仓库中暴露，使用环境变量管理
- 生产环境强烈建议使用代理服务器方式配置安全密钥
- 项目已支持后端传递安全密钥，这是推荐的配置方式
- JavaScript API和Web服务API需要分别配置和计费，请注意使用量
- 定期使用管理命令检查API使用情况
- 建议为开发和生产环境使用不同的API密钥