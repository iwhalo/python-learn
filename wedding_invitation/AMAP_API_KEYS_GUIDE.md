# 高德地图API密钥配置指南

## 概述

本项目区分两种类型的高德地图API密钥，以更好地满足不同的功能需求：

1. **Web服务API密钥**：用于后端地理编码和逆地理编码功能
2. **JavaScript API密钥**：用于前端地图展示功能

## API密钥类型详解

### Web服务API密钥 (AMAP_WEB_SERVICE_KEY)

- **用途**：后端地理编码、逆地理编码功能
- **调用方式**：服务器端内部调用
- **安全性**：相对安全，不会暴露给前端
- **功能**：
  - 地理编码：将地址转换为经纬度坐标
  - 逆地理编码：将经纬度转换为详细地址信息
  - 缓存机制管理
  - API调用统计

### JavaScript API密钥 (AMAP_JS_API_KEY)

- **用途**：前端地图展示功能
- **调用方式**：浏览器客户端调用
- **安全性**：需注意防范盗用
- **功能**：
  - 地图初始化和展示
  - 地图控件加载（缩放、鹰眼图等）
  - 标记点显示
  - 地图交互功能

## 配置方法

### 方法一：环境变量配置（推荐）

复制 `.env.example` 为 `.env`，并填写相应的API密钥：

```bash
# 高德地图Web服务API密钥（用于后端地理编码）
AMAP_WEB_SERVICE_KEY=your_web_service_api_key_here

# 高德地图JavaScript API密钥（用于前端地图展示）
AMAP_JS_API_KEY=your_js_api_key_here

# 高德地图安全密钥（JS API 2.0，必需）
AMAP_SECURITY_JS_CODE=your_security_js_code_here
```

### 方法二：直接在settings.py中配置

编辑 `wedding_invitation/settings.py`:

```python
# 高德地图Web服务API密钥（用于后端地理编码和逆地理编码功能）
AMAP_WEB_SERVICE_KEY = 'your_web_service_api_key_here'

# 高德地图JavaScript API密钥（用于前端地图展示功能）
AMAP_JS_API_KEY = 'your_js_api_key_here'

# 高德地图安全密钥（必需，用于JS API 2.0）
AMAP_SECURITY_JS_CODE = 'your_security_js_code_here'
```

## API密钥申请步骤

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册账号并登录
3. 进入控制台，创建新的应用
4. 为应用添加以下服务：
   - **Web服务API**：用于后端地理编码功能
   - **JavaScript API**：用于前端地图展示功能
5. 获取API密钥和安全密钥

## API密钥安全建议

1. **使用不同的密钥**：建议为Web服务API和JavaScript API分别申请不同的密钥
2. **域名绑定**：在高德平台配置JavaScript API密钥时，绑定您的域名以防止盗用
3. **IP白名单**：为Web服务API密钥配置IP白名单（如果适用）
4. **定期更换**：定期更换API密钥以增强安全性
5. **环境隔离**：为开发、测试、生产环境使用不同的API密钥

## 常见问题

### 1. 如何只申请一个API密钥？

可以申请一个API密钥，同时开通Web服务API和JavaScript API权限。在这种情况下，可以将同一个密钥同时用于 `AMAP_WEB_SERVICE_KEY` 和 `AMAP_JS_API_KEY`。

### 2. 为什么需要安全密钥？

安全密钥（AMAP_SECURITY_JS_CODE）是高德地图JS API 2.0的安全机制，用于防止API密钥在前端被直接暴露和滥用。

### 3. API密钥配置后如何验证？

启动项目后，在浏览器开发者工具的控制台中应该看不到API密钥相关的错误信息。

## 故障排除

### USERKEY_PLAT_NOMATCH 错误

这个错误表示API密钥类型与使用平台不匹配。请确保：
- JavaScript API密钥已正确申请并配置用于前端
- Web服务API密钥已正确申请并配置用于后端
- API密钥权限已正确开通

### 地理编码失败

检查 `AMAP_WEB_SERVICE_KEY` 是否正确配置，并确保该密钥具有Web服务API权限。

### 地图无法显示

检查 `AMAP_JS_API_KEY` 和 `AMAP_SECURITY_JS_CODE` 是否正确配置，并确保该密钥具有JavaScript API权限。