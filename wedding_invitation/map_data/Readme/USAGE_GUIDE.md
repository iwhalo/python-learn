# Map Data 包使用指南

## 概述
map_data 包是一个专门用于处理高德地图数据的 Python 包，包含城市编码、POI 分类和地理编码相关功能。该包为婚礼邀请系统提供了完整的地理位置处理能力，支持精确的地理编码、城市编码查询和POI分类处理。

## 目录结构
```
map_data/
├── __init__.py           # 包初始化文件，提供统一导入接口
├── map_data_utils.py     # 主要的数据管理工具
├── city_code_utils.py    # 城市编码处理工具
├── poi_utils.py          # POI分类处理工具
├── excel_handler.py      # Excel数据处理工具
├── models.py             # 数据模型定义
└── USAGE_GUIDE.md        # 本使用指南
```

## 主要功能模块

### 1. 城市编码处理 (city_code_utils)
- 根据城市名称获取城市编码(citycode)
- 根据城市名称获取区域编码(adcode)
- 城市名称与编码双向查询
- 支持模糊匹配和关键词搜索

### 2. POI分类处理 (poi_utils)
- 根据POI编码获取POI名称
- 根据POI名称获取POI编码
- POI关键词搜索
- POI分类层级管理

### 3. 数据模型 (models)
- 定义了 CityInfo, POICategory 等数据结构
- 提供类型安全的数据处理
- 支持数据验证和序列化

### 4. Excel数据处理 (excel_handler)
- 读取高德地图的Excel格式数据文件
- 支持POI分类和城市编码数据的导入导出
- 提供数据格式转换功能

## 使用方法

### 1. 基本导入
```python
# 导入整个包
from map_data import *

# 或者导入特定功能
from map_data import get_adcode, get_city_code, search_poi
from map_data.city_code_utils import CityCodeManager
from map_data.poi_utils import POICodeManager
```

### 2. 城市编码查询
```python
from map_data import get_adcode, get_city_code

# 获取城市编码
adcode = get_adcode("北京市")      # 返回区域编码
citycode = get_city_code("北京市")  # 返回城市编码

# 使用管理器类
from map_data.city_code_utils import CityCodeManager
manager = CityCodeManager()
city_info = manager.get_citycode_by_name("上海市")
```

### 3. POI分类查询
```python
from map_data import get_poi_name, search_poi

# 根据编码获取POI名称
poi_name = get_poi_name("110100")

# 搜索POI
food_pois = search_poi("餐饮")
```

### 4. 与地理编码API集成
```python
from invitation.views import geocode_address
from map_data import get_adcode

# 使用城市编码进行地理编码
city_name = "北京市"
adcode = get_adcode(city_name)
result = geocode_address(
    address="北京市朝阳区阜通东大街6号",
    city=adcode,
    api_key=settings.AMAP_API_KEY
)
```

## 与婚礼邀请系统集成示例

### 1. 婚礼地点地理编码
```python
from invitation.views import geocode_address
from map_data import get_adcode
from django.conf import settings

def process_wedding_location(wedding_event):
    """处理婚礼地点的地理编码，提高精度"""
    if not wedding_event.address:
        return None
        
    # 如果知道城市，使用城市编码提高精度
    if wedding_event.city:
        city_adcode = get_adcode(wedding_event.city)
        geocoding_result = geocode_address(
            address=wedding_event.address,
            city=city_adcode,  # 使用城市编码提高精度
            api_key=settings.AMAP_API_KEY,
            use_cache=True  # 启用缓存
        )
    else:
        # 不知道城市时直接使用地址
        geocoding_result = geocode_address(
            address=wedding_event.address,
            api_key=settings.AMAP_API_KEY,
            use_cache=True
        )
        
    if geocoding_result:
        # 使用地理编码结果更新地图配置
        map_config = {
            'center_lat': geocoding_result['latitude'],
            'center_lng': geocoding_result['longitude'],
            'zoom': 15,
            'marker_title': wedding_event.venue or wedding_event.title,
            'marker_content': wedding_event.address,
            'confidence': geocoding_result['confidence'],
            'geocoding_details': geocoding_result
        }
        return map_config
    else:
        # 地理编码失败时返回默认配置
        return {
            'center_lat': 39.90923,
            'center_lng': 116.397428,
            'zoom': 12,
            'marker_title': '婚礼地点',
            'marker_content': '地理编码失败',
            'confidence': 0,
            'geocoding_details': {}
        }
```

### 2. 地图页面中使用城市编码
```python
def map_view(request):
    # 获取婚礼事件
    from invitation.models import WeddingEvent
    wedding_event = WeddingEvent.objects.first()
    
    if wedding_event and wedding_event.address:
        # 使用城市编码进行更精确的地理编码
        if wedding_event.city:
            city_adcode = get_adcode(wedding_event.city)
            geocoding_result = geocode_address(
                address=wedding_event.address,
                city=city_adcode,
                api_key=settings.AMAP_API_KEY
            )
        else:
            geocoding_result = geocode_address(
                address=wedding_event.address,
                api_key=settings.AMAP_API_KEY
            )
        
        if geocoding_result:
            map_config = {
                'center_lat': geocoding_result['latitude'],
                'center_lng': geocoding_result['longitude'],
                'zoom': 15,
                'confidence': geocoding_result['confidence'],
                'geocoding_details': geocoding_result
            }
        else:
            # 使用默认坐标
            map_config = {
                'center_lat': 39.90923,
                'center_lng': 116.397428,
                'zoom': 12,
                'confidence': 0,
                'geocoding_details': {}
            }
    else:
        # 没有婚礼事件时使用默认配置
        map_config = {
            'center_lat': 39.90923,
            'center_lng': 116.397428,
            'zoom': 12,
            'confidence': 0,
            'geocoding_details': {}
        }
    
    context = {
        'wedding_event': wedding_event,
        'amap_api_key': settings.AMAP_API_KEY,
        'amap_security_js_code': getattr(settings, 'AMAP_SECURITY_JS_CODE', ''),
        'map_config': map_config
    }
    
    return render(request, 'map.html', context)
```

### 3. 逆地理编码获取周边信息
```python
from invitation.views import reverse_geocode

def get_nearby_venues(lat, lng):
    """获取婚礼地点附近的 venues 信息"""
    # 获取附近的餐饮场所
    restaurants = reverse_geocode(
        lat=lat,
        lng=lng,
        api_key=settings.AMAP_API_KEY,
        poitype="餐饮服务",  # 搜索餐饮场所
        radius=2000,  # 2公里范围内
        extensions='all'
    )
    
    # 获取附近的交通设施
    transport = reverse_geocode(
        lat=lat,
        lng=lng,
        api_key=settings.AMAP_API_KEY,
        poitype="交通设施服务",  # 搜索交通设施
        radius=1000,
        extensions='all'
    )
    
    return {
        'restaurants': restaurants,
        'transport': transport
    }
```

### 4. 婚礼城市信息处理
```python
def process_wedding_city_info(wedding_event):
    """处理婚礼所在城市的信息"""
    if not wedding_event.city:
        return None
        
    # 获取城市编码信息
    city_adcode = get_adcode(wedding_event.city)
    city_code = get_city_code(wedding_event.city)
    
    if not city_adcode:
        return None
        
    # 使用城市编码获取更详细的信息
    geocoding_result = geocode_address(
        address=f"{wedding_event.city}市政府",
        city=city_adcode,
        api_key=settings.AMAP_API_KEY
    )
    
    if geocoding_result:
        return {
            'city_name': wedding_event.city,
            'city_adcode': city_adcode,
            'city_code': city_code,
            'center_lat': geocoding_result['latitude'],
            'center_lng': geocoding_result['longitude'],
            'confidence': geocoding_result['confidence']
        }
    else:
        return {
            'city_name': wedding_event.city,
            'city_adcode': city_adcode,
            'city_code': city_code,
            'center_lat': 0,
            'center_lng': 0,
            'confidence': 0
        }
```

### 5. POI搜索功能
```python
def search_nearby_facilities(wedding_address, city_name):
    """搜索婚礼地点附近的设施"""
    # 首先获取婚礼地点的坐标
    city_adcode = get_adcode(city_name)
    geocoding_result = geocode_address(
        address=wedding_address,
        city=city_adcode,
        api_key=settings.AMAP_API_KEY
    )
    
    if not geocoding_result:
        return None
        
    lat = geocoding_result['latitude']
    lng = geocoding_result['longitude']
    
    # 搜索附近的酒店
    hotels = reverse_geocode(
        lat=lat,
        lng=lng,
        api_key=settings.AMAP_API_KEY,
        poitype="住宿服务",
        radius=3000,
        extensions='all'
    )
    
    # 搜索附近的停车场
    parking = reverse_geocode(
        lat=lat,
        lng=lng,
        api_key=settings.AMAP_API_KEY,
        poitype="停车场",
        radius=1000,
        extensions='all'
    )
    
    return {
        'hotels': hotels,
        'parking': parking,
        'location': {
            'lat': lat,
            'lng': lng
        }
    }
```

## 高级功能

### 1. Excel数据处理
```python
from map_data.excel_handler import excel_handler

# 加载POI数据
poi_data = excel_handler.load_poi_data()

# 加载城市数据
city_data = excel_handler.load_city_data()

# 导出数据
excel_handler.export_poi_data(poi_data, "output_poi.xlsx")
excel_handler.export_city_data(city_data, "output_city.xlsx")
```

### 2. 自定义数据源
```python
from map_data.map_data_utils import MapDataManager
from map_data.poi_utils import POICodeManager
from map_data.city_code_utils import CityCodeManager

# 使用自定义数据目录
custom_manager = MapDataManager(data_dir="/path/to/custom/data")
```

### 3. 数据模型使用
```python
from map_data.models import CityInfo, POICategory

# 创建城市信息对象
city = CityInfo(
    name="北京市",
    adcode="110000",
    citycode="010",
    center="116.407170,39.904623",
    level="province"
)

# 创建POI分类对象
poi = POICategory(
    code="110100",
    name="餐饮服务",
    english_name="Catering Service"
)
```

## 性能优化建议

### 1. 合理使用缓存
```python
# 在大量地理编码请求时启用缓存
result = geocode_address(
    address="地址",
    api_key=settings.AMAP_API_KEY,
    use_cache=True  # 启用缓存
)
```

### 2. 控制API调用频率
```python
# 设置每日调用限制
result = geocode_address(
    address="地址",
    api_key=settings.AMAP_API_KEY,
    daily_limit=1000  # 每日最多1000次调用
)
```

## 注意事项
1. 确保已安装 pandas 和 openpyxl 库以支持 Excel 文件处理
2. 数据文件路径默认为 `map_files` 目录
3. 包含缓存机制，首次加载可能较慢
4. 支持中文城市名称和英文POI名称的搜索
5. 在婚礼邀请系统中使用时，建议结合城市编码以提高地理编码精度
6. 地理编码结果包含置信度评分，可根据置信度决定是否需要人工验证
7. 逆地理编码可用于获取地点周边的POI信息，丰富婚礼地点的相关信息
8. 城市编码查询支持模糊匹配，但精确匹配性能更好
9. 建议在生产环境中对常用的地理编码结果进行持久化缓存