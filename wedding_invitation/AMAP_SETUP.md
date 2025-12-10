# 高德地图API配置指南

## 如何获取高德地图API密钥

1. 访问高德开放平台官网：https://lbs.amap.com/
2. 注册账号并登录
3. 进入控制台，创建一个新的应用
4. 在应用中创建一个Key，选择Web服务API类型
5. 复制生成的API密钥

## 配置API密钥

### 方法一：环境变量（推荐）

在系统环境中设置环境变量：

**Windows:**
```cmd
set AMAP_API_KEY=你的API密钥
```

**Linux/macOS:**
```bash
export AMAP_API_KEY=你的API密钥
```

### 方法二：直接修改settings.py

如果不想使用环境变量，可以直接在 `wedding_invitation/settings.py` 文件中修改：

```python
AMAP_API_KEY = '你的API密钥'
```

## 注意事项

- API密钥具有有效期和调用次数限制
- 请妥善保管API密钥，避免泄露
- 申请API密钥时请选择"Web服务"类型，否则会出现USERKEY_PLAT_NOMATCH错误
- 高德地图Web服务API需要在高德开放平台绑定域名才能正常使用
- 如果API密钥无效，地图将显示默认位置（北京天安门）