# 婚礼邀请系统项目架构文档

## 项目概述

婚礼邀请系统是一个基于Python Django框架开发的电子请柬系统，集成了高德地图API，提供地理编码和逆地理编码功能，支持精确的位置展示和地址解析。

## 项目架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端界面层     │    │   Django框架层   │    │   数据存储层     │
│                 │    │                 │    │                 │
│  HTML Templates │◄──►│   Views         │◄──►│  Database       │
│  CSS/JS         │    │   URL Routing   │    │  Models         │
│  AJAX Requests  │    │   Middleware    │    │  Admin          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌─────────────────┐             │
         └──────────────►│   业务逻辑层     │◄────────────┘
                         │                 │
                         │  Invitation App │
                         │  Map Data Package│
                         │  Geocoding Cache│
                         │  API Stats      │
                         └─────────────────┘
                                          │
                         ┌─────────────────┤
                         │   外部服务层     │
                         │                 │
                         │  高德地图API     │
                         │  Web Services   │
                         │  Geocoding API  │
                         └─────────────────┘
```

## 模块结构

### 1. 核心应用模块 (invitation/)

```
invitation/
├── models.py           # 数据模型定义
├── views.py           # 视图函数和业务逻辑
├── urls.py            # URL路由配置
├── admin.py           # Django管理后台配置
├── apps.py            # 应用配置
└── templatetags/      # 自定义模板标签
    └── custom_filters.py
```

#### 1.1 Models (数据模型)
- **WeddingEvent**: 婚礼活动信息模型
- **Guest**: 宾客信息模型
- **GalleryImage**: 相册图片模型
- **PageVisit**: 页面访问统计模型
- **GeocodingCache**: 地理编码缓存模型
- **APIUsageStats**: API使用统计模型

#### 1.2 Views (视图函数)
- **index()**: 首页视图
- **rsvp_form()**: RSVP表单页面
- **submit_rsvp()**: RSVP提交处理
- **countdown()**: 倒计时页面
- **gallery()**: 相册页面
- **map_location()**: 地图位置页面
- **guest_list()**: 宾客列表页面
- **guest_stats_api()**: 宾客统计API
- **geocode_address()**: 地理编码函数
- **reverse_geocode()**: 逆地理编码函数
- **calculate_confidence()**: 置信度计算函数

#### 1.3 URL路由
- `/`: 首页
- `/rsvp/`: RSVP表单
- `/countdown/`: 倒计时
- `/gallery/`: 相册
- `/map/`: 地图页面
- `/guest-list/`: 宾客列表
- `/api/guest-stats/`: 宾客统计API

### 2. 地图数据处理模块 (map_data/)

```
map_data/
├── __init__.py        # 统一导入接口
├── map_data_utils.py  # 数据管理工具
├── city_code_utils.py # 城市编码处理
├── poi_utils.py       # POI分类处理
├── excel_handler.py   # Excel数据处理
├── models.py          # 数据模型
└── Readme/           # 文档
```

#### 2.1 功能模块
- **CityCodeManager**: 城市编码管理器
- **POICodeManager**: POI分类管理器
- **MapDataManager**: 地图数据管理器
- **ExcelHandler**: Excel数据处理器

#### 2.2 统一接口
- `get_adcode()`: 获取区域编码
- `get_city_code()`: 获取城市编码
- `get_poi_name()`: 获取POI名称
- `search_poi()`: 搜索POI

### 3. 前端界面模块 (templates/, static/)

#### 3.1 模板文件
- **index.html**: 首页模板
- **rsvp.html**: RSVP表单模板
- **map.html**: 地图页面模板
- **gallery.html**: 相册模板
- **countdown.html**: 倒计时模板
- **guest_list.html**: 宾客列表模板

#### 3.2 静态资源
- **style.css**: 样式文件
- **JavaScript**: 地图API加载和交互

### 4. 项目配置 (wedding_invitation/)

```
wedding_invitation/
├── settings.py        # 项目设置
├── urls.py           # 项目路由
├── wsgi.py           # WSGI配置
└── asgi.py           # ASGI配置
```

## 模块交互关系

### 1. 请求处理流程

```
Client Request
       │
       ▼
Django URL Router
       │
       ▼
   View Function
       │
       ├─► Query Database (Models)
       ├─► Call Geocoding API (map_data)
       ├─► Process Business Logic
       └─► Render Template
       │
       ▼
   HTTP Response
```

### 2. 地理编码处理流程

```
Address String
       │
       ▼
   get_adcode() (map_data)
       │
       ▼
geocode_address() (views)
       │
       ├─► Check Cache (GeocodingCache)
       ├─► Call AMap API
       ├─► Calculate Confidence
       └─► Store Result
       │
       ▼
   Coordinates
```

### 3. 数据流向

```
Frontend (Templates)
       │
       ▲
Views (Business Logic)
       │
       ▼
Models (Database)
       │
       ◄─── Geocoding Cache ───► map_data
       │                            │
       └────────────────────────────┘
```

## 核心功能实现

### 1. 地理编码功能
- **输入**: 地址字符串、城市信息
- **处理**: 通过高德API进行地理编码
- **输出**: 经纬度坐标、置信度评分
- **缓存**: 使用GeocodingCache模型缓存结果

### 2. 逆地理编码功能
- **输入**: 经纬度坐标
- **处理**: 通过高德API进行逆地理编码
- **输出**: 详细地址信息、POI信息

### 3. 城市编码处理
- **功能**: 城市名称与编码互转
- **数据源**: Excel格式的城市编码表
- **缓存**: 内存缓存提高查询性能

### 4. POI分类处理
- **功能**: POI编码与名称互转
- **数据源**: Excel格式的POI分类表
- **搜索**: 支持关键词搜索

## 技术栈

### 后端技术
- **框架**: Django 4.x
- **语言**: Python 3.8+
- **数据库**: SQLite (默认), 支持 PostgreSQL/MySQL
- **API**: 高德地图Web服务API

### 前端技术
- **模板引擎**: Django Template
- **样式**: CSS3
- **脚本**: JavaScript
- **地图**: 高德地图JS API 2.0

### 数据处理
- **库**: pandas, openpyxl
- **格式**: Excel, JSON
- **缓存**: Django ORM

## 部署架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Server    │    │  Application    │    │   External      │
│   (Nginx)       │    │   (Django)      │    │   Services      │
│                 │    │                 │    │                 │
│ Static Files    │◄──►│ Views           │◄──►│ AMap API        │
│ SSL Termination │    │ URL Routing     │    │ Web Services    │
│ Load Balance    │    │ Authentication  │    │ Geocoding       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌─────────────────┐             │
         └──────────────►│   Database      │◄────────────┘
                         │                 │
                         │ PostgreSQL/     │
                         │ MySQL/SQLite    │
                         │ Redis (Cache)   │
                         └─────────────────┘
```

## 安全措施

1. **API密钥管理**: 环境变量存储，支持代理服务器配置
2. **输入验证**: 地址和坐标输入验证
3. **访问控制**: Django认证系统
4. **SQL注入防护**: Django ORM自动防护
5. **XSS防护**: Django模板自动转义

## 性能优化

1. **缓存机制**: 地理编码结果缓存
2. **数据库索引**: 优化查询性能
3. **静态文件优化**: CDN支持
4. **API调用限制**: 防止滥用
5. **异步处理**: 支持异步操作

## 监控和维护

1. **API使用统计**: 跟踪调用次数和成功率
2. **错误日志**: 详细的错误记录
3. **性能监控**: 响应时间监控
4. **缓存管理**: 定期清理过期数据
5. **管理命令**: 提供便捷的管理工具