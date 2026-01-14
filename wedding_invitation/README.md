# 婚礼邀请电子请柬系统

这是一个基于Python和Django框架开发的婚礼邀请电子请柬系统，具有现代化的设计和丰富的功能。系统集成了高德地图API，支持精确的地理编码和逆地理编码功能，能够将婚礼地址转换为地图坐标并在地图上准确显示。

## 功能特性

- **精美页面设计**: 使用现代CSS样式，响应式布局，适配各种设备
- **婚礼信息展示**: 展示婚礼时间、地点、新人姓名等信息
- **倒计时功能**: 实时显示距离婚礼还有多少天
- **RSVP回复**: 宾客可以确认出席并留下祝福
- **相册展示**: 展示婚纱照、订婚照等纪念照片，支持自定义相册配置
- **地图位置**: 显示婚礼举办地点及交通指南，集成高德地图API
- **地理编码功能**: 支持地址到坐标的精确转换，包含置信度评估
- **访问统计**: 记录网站访问量和宾客回复情况
- **数据管理**: 通过Django管理后台轻松管理所有内容

## 技术栈

- **后端**: Python + Django
- **前端**: HTML5, CSS3, JavaScript
- **数据库**: SQLite (默认) / PostgreSQL / MySQL
- **地图API**: 高德地图API (地理编码/逆地理编码)
- **字体**: Google Fonts Noto Serif SC
- **地理数据**: 城市编码(citycode/adcode)、POI分类数据

## 项目结构

```
wedding_invitation/
├── manage.py
├── .env.example                 # 环境变量配置示例
├── wedding_invitation/          # 项目配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── invitation/                  # 邀请应用
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                # 数据模型 (WeddingEvent, Guest, GalleryImage等)
│   ├── views.py                 # 视图函数 (包含地理编码功能)
│   ├── urls.py
│   ├── templatetags/            # 自定义模板标签
│   │   └── custom_filters.py
│   └── migrations/
├── map_data/                    # 地图数据处理包
│   ├── __init__.py              # 统一导入接口
│   ├── map_data_utils.py        # 地图数据管理工具
│   ├── city_code_utils.py       # 城市编码处理工具
│   ├── poi_utils.py             # POI分类处理工具
│   ├── excel_handler.py         # Excel数据处理
│   ├── models.py                # 地图数据模型
│   └── Readme/                  # 地图数据文档
│       ├── CITY_CODE_README.md
│       ├── MAP_DATA_GUIDE.md
│       ├── USAGE_GUIDE.md
│       ├── city_code_guide.md
│       └── sample_city_codes.json
├── templates/                   # 模板文件
│   ├── index.html              # 首页
│   ├── rsvp.html               # RSVP回复页面
│   ├── countdown.html          # 倒计时页面
│   ├── gallery.html            # 相册页面
│   ├── map.html                # 地图页面
│   └── guest_list.html         # 宾客列表页面
├── static/css/
│   └── style.css
├── media/                      # 媒体文件目录
│   ├── gallery/                # 相册图片
│   └── wedding_covers/         # 封面图片
├── requirements.txt
├── README.md
├── AMAP_CONFIG_GUIDE.md        # 高德地图API配置指南
├── AMAP_INTEGRATION_README.md  # 高德地图集成说明
├── AMAP_SETUP.md               # 高德地图快速配置
├── API_KEY_SETUP.md            # API密钥配置指南
├── gallery_config.md           # 相册配置说明
├── populate_data.py            # 填充演示数据脚本
├── run_migrations.py           # 运行迁移脚本
├── create_pagevisit_table.py   # 创建访问统计表
├── test_geocoding.py           # 地理编码测试
└── db.sqlite3
```

## 快速开始

1. **克隆项目并进入目录**:
   ```bash
   git clone <repository-url>
   cd wedding_invitation
   ```

2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**:
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 中配置高德地图API密钥
   ```bash
   AMAP_API_KEY=your_actual_amap_api_key
   AMAP_SECURITY_JS_CODE=your_security_js_code  # 可选，但推荐配置
   DEBUG=True
   SECRET_KEY=your_secret_key
   ```

4. **运行数据库迁移**:
   ```bash
   python manage.py migrate
   ```

5. **创建超级用户** (可选):
   ```bash
   python manage.py createsuperuser
   ```

6. **填充演示数据** (可选):
   ```bash
   python populate_data.py
   ```

7. **启动开发服务器**:
   ```bash
   python manage.py runserver
   ```

8. **访问网站**:
   打开浏览器访问 http://127.0.0.1:8000/

## 高德地图API配置

### 申请API密钥

1. 访问 [高德开放平台](https://lbs.amap.com/) 注册账号
2. 登录后进入控制台，创建新应用
3. 选择「Web端(JSAPI)」平台类型
4. 创建密钥时勾选「JavaScript API」和「Web服务API」
5. 获取API Key和安全密钥(jscode)

### 配置API密钥

系统支持多种配置方式，推荐使用环境变量方式。项目区分两种类型的API密钥：
- Web服务API密钥：用于后端地理编码和逆地理编码功能
- JavaScript API密钥：用于前端地图展示功能

**方式一：环境变量（推荐）**
- 在 `.env` 文件中配置：
```bash
AMAP_WEB_SERVICE_KEY=your_web_service_api_key_here  # 用于后端地理编码
AMAP_JS_API_KEY=your_js_api_key_here              # 用于前端地图展示
AMAP_SECURITY_JS_CODE=your_security_code_here     # 安全密钥（必需）
```

**方式二：直接在settings.py中配置**
- 编辑 `wedding_invitation/settings.py`:
```python
AMAP_WEB_SERVICE_KEY = 'your_web_service_api_key_here'  # 用于后端地理编码
AMAP_JS_API_KEY = 'your_js_api_key_here'              # 用于前端地图展示
AMAP_SECURITY_JS_CODE = 'your_security_code_here'     # 安全密钥（必需）
```

### 地理编码功能

系统集成了完整的地理编码功能：
- **地理编码**: 将地址转换为经纬度坐标
- **逆地理编码**: 将经纬度转换为详细地址信息
- **置信度评估**: 根据匹配级别计算地理编码的准确性
- **缓存机制**: 避免重复API调用，提高性能
- **API限制管理**: 跟踪调用次数，防止超出配额

## 管理后台

访问 http://127.0.0.1:8000/admin/ 可以管理：
- 婚礼信息（时间、地点、新人信息等）
- 宾客信息（RSVP回复、联系方式等）
- 相册内容（上传和管理照片）
- 访问统计数据

## 地图数据功能

项目包含专门的 `map_data` 包，提供以下功能：

### 城市编码处理
- 支持城市编码(citycode)和区域编码(adcode)查询
- 提供全国主要城市的编码对照表
- 支持关键词搜索城市

### POI分类处理
- 包含高德地图POI分类与编码对照表
- 支持POI类型搜索和分类
- 提供中英文POI名称对照

### 使用示例

```python
from map_data import get_adcode, get_city_code, search_poi

# 获取城市编码
beijing_adcode = get_adcode("北京市")      # 返回: 110000
shanghai_code = get_city_code("上海市")    # 返回: 021

# 搜索POI分类
restaurants = search_poi("餐饮")          # 搜索所有餐饮类POI
```

## 系统管理命令

项目提供了多个管理命令：

- `python manage.py cleanup_geocoding_cache` - 清理过期的地理编码缓存
- `python manage.py show_api_stats` - 查看API使用统计
- `python manage.py setup_gallery` - 初始化相册目录

## 自定义配置

您可以根据需要修改以下内容：

- 在Django管理后台中编辑婚礼信息
- 修改模板文件以调整页面布局
- 更换静态资源文件以定制样式
- 添加更多相册图片
- 配置高德地图API密钥以启用地图功能
- 调整地图显示参数（缩放级别、标记样式等）

## 部署说明

在生产环境中部署时，建议:

1. 使用PostgreSQL或MySQL替换SQLite
2. 配置静态文件服务（如Nginx）
3. 设置适当的中间件和安全选项
4. 配置邮件服务以发送确认邮件
5. 设置环境变量以保护敏感信息
6. 配置反向代理以处理高德地图安全密钥

## 环境变量配置

项目使用以下环境变量：

- `AMAP_WEB_SERVICE_KEY`: 高德地图Web服务API密钥（必需，用于后端地理编码）
- `AMAP_JS_API_KEY`: 高德地图JavaScript API密钥（必需，用于前端地图展示）
- `AMAP_SECURITY_JS_CODE`: 高德地图安全密钥（必需）
- `DEBUG`: 调试模式开关
- `SECRET_KEY`: Django安全密钥
- `ALLOWED_HOSTS`: 允许的主机列表

## 许可证

此项目仅供学习和参考使用。