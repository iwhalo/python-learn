# 高德地图数据使用指南

## 概述
本指南介绍了项目中使用的高德地图相关数据，包括城市编码(citycode/adcode)和POI分类编码的使用方法。所有地图数据处理功能都集中在 `map_data` 包中，提供了一套完整的地理信息处理解决方案。

## 目录
- [1. map_data 包结构](#1-map_data-包结构)
- [2. 城市编码(citycode/adcode)](#2-城市编码citycodeadcode)
- [3. POI分类编码](#3-poi分类编码)
- [4. 数据文件说明](#4-数据文件说明)
- [5. 使用方法](#5-使用方法)
- [6. 实际应用示例](#6-实际应用示例)
- [7. 性能优化](#7-性能优化)
- [8. 错误处理](#8-错误处理)
- [9. 最佳实践](#9-最佳实践)

## 1. map_data 包结构

### 1.1 目录结构
```
map_data/                           # 地图数据处理包
├── __init__.py                     # 包初始化文件，提供统一导入接口
├── map_data_utils.py               # 主要的数据管理工具
├── city_code_utils.py              # 城市编码处理工具
├── poi_utils.py                    # POI分类处理工具
├── excel_handler.py                # Excel数据处理工具
├── models.py                       # 数据模型定义
├── Readme/                         # 文档目录
│   ├── CITY_CODE_README.md         # 城市编码使用说明
│   ├── MAP_DATA_GUIDE.md           # 地图数据使用指南
│   ├── USAGE_GUIDE.md              # 使用指南
│   ├── city_code_guide.md          # 城市编码指南
│   └── sample_city_codes.json      # 城市编码示例数据
└── __pycache__/                    # Python缓存目录
```

### 1.2 统一导入接口
map_data 包提供了统一的导入接口，可通过以下方式使用：
```python
# 统一导入
from map_data import get_adcode, get_city_code, get_poi_name, search_poi

# 导入管理器类
from map_data import CityCodeManager, POICodeManager, MapDataManager
```

## 2. 城市编码(citycode/adcode)

### 2.1 基本概念
- **citycode**: 城市编码，通常对应电话区号，如北京010、上海021
- **adcode**: 行政区划代码，用于标识行政区域，如北京市110000、上海市310000

### 2.2 使用场景
- 地理编码API中指定查询城市
- 逆地理编码API中获取区域信息
- 地图展示时的区域定位
- POI搜索和分类过滤

### 2.3 工具函数
```python
from map_data import get_city_code, get_adcode

# 获取城市编码
beijing_code = get_city_code("北京市")  # 返回: 010
shanghai_code = get_city_code("上海市")  # 返回: 021

# 获取区域编码
beijing_adcode = get_adcode("北京市")  # 返回: 110000
shanghai_adcode = get_adcode("上海市")  # 返回: 310000
```

### 2.4 高级城市编码功能
```python
from map_data.city_code_utils import CityCodeManager

# 创建管理器实例
manager = CityCodeManager()

# 精确匹配城市编码
adcode = manager.get_adcode_by_name("北京市")
citycode = manager.get_citycode_by_name("北京市")

# 模糊搜索城市
results = manager.search_cities_by_keyword("北京")

# 根据adcode获取城市信息
city_info = manager.get_city_info_by_adcode("110105")  # 朝阳区信息
```

## 3. POI分类编码

### 3.1 基本概念
POI(Point of Interest)分类编码用于标识不同类型的地点，如餐饮、住宿、购物等。POI分类编码有助于在逆地理编码中过滤和分类兴趣点。

### 3.2 使用场景
- 逆地理编码API中指定POI类型
- 搜索周边特定类型的地点
- POI信息筛选和分类
- 地图标记类型控制

### 3.3 工具函数
```python
from map_data import get_poi_name, search_poi

# 根据编码获取POI名称
poi_name = get_poi_name("110100")  # 餐饮服务

# 搜索POI
food_pois = search_poi("餐饮")  # 搜索所有餐饮类POI
```

### 3.4 高级POI功能
```python
from map_data.poi_utils import POICodeManager

# 创建POI管理器
poi_manager = POICodeManager()

# 获取POI信息
poi_name = poi_manager.get_poi_name_by_code("110100")
poi_code = poi_manager.get_poi_code_by_name("餐饮服务")

# 搜索POI分类
restaurants = poi_manager.search_poi_by_keyword("餐饮")

# 获取POI分类层级
poi_hierarchy = poi_manager.get_poi_hierarchy("110100")
```

## 4. 数据文件说明

### 4.1 城市编码数据
- **来源**: `map_files/AMap_adcode_citycode/AMap_adcode_citycode.xlsx`
- **包含**: 中国各省市县的adcode和citycode对照表
- **格式**: Excel文件，包含城市名称、区域编码、城市编码等信息
- **数据结构**: 城市名称、adcode、citycode、中心坐标、行政级别等

### 4.2 POI分类数据
- **来源**: `map_files/Amap_poicode/高德POI分类与编码（中英文）_V1.06_20230208.xlsx`
- **包含**: 高德地图POI分类与编码对照表
- **格式**: Excel文件，包含POI编码、中文名称、英文名称等信息
- **数据结构**: POI编码、中文名称、英文名称、父级分类、层级信息等

### 4.3 数据文件管理
```python
from map_data.excel_handler import excel_handler

# 加载城市数据
city_data = excel_handler.load_city_data()

# 加载POI数据
poi_data = excel_handler.load_poi_data()

# 导出数据
excel_handler.export_city_data(city_data, "output_city.xlsx")
excel_handler.export_poi_data(poi_data, "output_poi.xlsx")
```

## 5. 使用方法

### 5.1 城市编码查询
```python
from map_data.city_code_utils import CityCodeManager

manager = CityCodeManager()

# 获取城市编码
city_code = manager.get_citycode_by_name("北京市")
adcode = manager.get_adcode_by_name("北京市")

# 搜索城市
cities = manager.search_cities_by_keyword("北京")

# 获取城市详细信息
city_detail = manager.get_city_detail("北京市")
```

### 5.2 POI分类查询
```python
from map_data.poi_utils import POICodeManager

poi_manager = POICodeManager()

# 获取POI信息
poi_name = poi_manager.get_poi_name_by_code("110100")
poi_code = poi_manager.get_poi_code_by_name("餐饮服务")

# 搜索POI
restaurants = poi_manager.search_poi_by_keyword("餐饮")

# 获取POI分类树
poi_tree = poi_manager.get_poi_category_tree()
```

### 5.3 在地理编码API中使用
```python
from invitation.views import geocode_address, reverse_geocode
from map_data import get_adcode

# 地理编码 - 使用城市编码
city_name = "北京市"
adcode = get_adcode(city_name)
result = geocode_address(
    address="北京市朝阳区阜通东大街6号",
    city=adcode,  # 使用adcode参数指定查询城市
    api_key=settings.AMAP_WEB_SERVICE_KEY,
    use_cache=True,  # 启用缓存
    daily_limit=1000  # 每日调用限制
)

# 逆地理编码 - 使用POI类型
result = reverse_geocode(
    lat=39.997213,
    lng=116.481938,
    api_key=settings.AMAP_WEB_SERVICE_KEY,
    poitype="餐饮服务",  # 指定POI类型
    radius=1000,  # 搜索半径
    extensions='all',  # 获取详细信息
    use_cache=True,  # 启用缓存
    daily_limit=1000  # 每日调用限制
)
```

## 6. 实际应用示例

### 6.1 在地图页面中使用
在地图页面中，可以根据用户输入的城市名称自动获取对应的编码：

```python
def map_view(request):
    # 假设用户输入了城市名称
    city_name = request.GET.get('city', '北京市')
    
    # 获取城市编码用于地理编码查询
    city_adcode = get_adcode(city_name)
    
    # 使用城市编码进行地理编码
    geocode_result = geocode_address(
        address=f"{city_name}市中心",
        city=city_adcode,
        api_key=settings.AMAP_WEB_SERVICE_KEY,
        use_cache=True  # 启用缓存
    )
    
    # 在模板中传递编码信息
    context = {
        'city_info': geocode_result,
        'city_name': city_name,
        'city_adcode': city_adcode,
        'confidence': geocode_result.get('confidence', 0) if geocode_result else 0
    }
    
    return render(request, 'map.html', context)
```

### 6.2 POI搜索功能
在逆地理编码中使用POI分类编码来获取特定类型的地点信息：

```python
def nearby_pois(request):
    lat = float(request.GET.get('lat', 0))
    lng = float(request.GET.get('lng', 0))
    poi_type = request.GET.get('type', '餐饮服务')
    radius = int(request.GET.get('radius', 1000))
    
    # 获取附近的特定类型POI
    result = reverse_geocode(
        lat=lat,
        lng=lng,
        api_key=settings.AMAP_WEB_SERVICE_KEY,
        poitype=poi_type,  # 使用POI分类
        radius=radius,  # 指定搜索半径
        extensions='all'
    )
    
    return JsonResponse(result)
```

### 6.3 婚礼地点地理编码
在婚礼邀请系统中使用城市编码提高地理编码精度：

```python
def process_wedding_location(wedding_event):
    """处理婚礼地点的地理编码"""
    if not wedding_event.address:
        return None
        
    # 如果知道城市，使用城市编码提高精度
    if wedding_event.city:
        city_adcode = get_adcode(wedding_event.city)
        geocoding_result = geocode_address(
            address=wedding_event.address,
            city=city_adcode,  # 使用城市编码提高精度
            api_key=settings.AMAP_WEB_SERVICE_KEY,
            use_cache=True
        )
    else:
        # 不知道城市时直接使用地址
        geocoding_result = geocode_address(
            address=wedding_event.address,
            api_key=settings.AMAP_WEB_SERVICE_KEY,
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

## 7. 性能优化

### 7.1 缓存机制
map_data包内置了智能缓存机制：

```python
# 城市编码查询结果会被缓存
adcode = get_adcode("北京市")  # 首次查询，加载数据
adcode = get_adcode("北京市")  # 后续查询直接从缓存获取

# POI搜索结果也会被缓存
restaurants = search_poi("餐饮")  # 首次查询
restaurants = search_poi("餐饮")  # 从缓存获取
```

### 7.2 数据预加载
为提高性能，可以预先加载数据：

```python
from map_data.map_data_utils import MapDataManager

# 预加载所有数据
manager = MapDataManager()
manager.preload_all_data()  # 预加载城市编码和POI数据
```

## 8. 错误处理

### 8.1 异常处理
```python
try:
    adcode = get_adcode("未知城市")
    if adcode is None:
        print("未找到对应的城市编码")
except Exception as e:
    print(f"查询过程中发生错误: {e}")
```

### 8.2 数据验证
```python
# 验证城市编码是否存在
if get_adcode("北京市"):
    # 城市编码存在，继续处理
    pass
else:
    # 城市编码不存在，使用默认值或错误处理
    pass
```

## 9. 最佳实践

### 9.1 使用建议
1. **优先使用统一导入接口**：推荐使用 `from map_data import ...` 方式导入功能
2. **合理使用城市编码**：在地理编码时使用adcode参数提高精度
3. **启用缓存机制**：使用`use_cache=True`参数减少重复API调用
4. **处理异常情况**：始终检查返回值，处理可能的None情况
5. **数据更新**：定期更新Excel数据文件以获取最新的编码信息

### 9.2 性能优化
1. **批量处理**：对于大量地理编码请求，考虑批量处理
2. **缓存策略**：合理使用缓存，平衡内存使用和查询速度
3. **API调用限制**：注意API调用频率限制，避免超出配额
4. **异步处理**：对于大量数据处理，考虑使用异步方式

### 9.3 安全考虑
1. **数据来源验证**：确保Excel数据文件来源可靠
2. **输入验证**：验证用户输入，防止恶意查询
3. **API密钥保护**：合理配置和保护API密钥

## 注意事项
1. 数据文件需要安装pandas和openpyxl库才能读取Excel格式
2. 城市编码和POI分类编码可能随高德地图更新而变化
3. 建议定期更新数据文件以获取最新的编码信息
4. 在生产环境中考虑缓存常用的城市编码和POI分类信息以提高性能
5. 所有地图数据功能都已集中到 map_data 包中，便于维护和管理
6. 城市编码查询支持模糊匹配，但精确匹配性能更好
7. POI分类数据包含层级关系，可用于分类统计和过滤
8. 数据加载在首次使用时可能较慢，后续使用会显著提升性能

## 参考资料
- 高德开放平台城市编码表：https://lbs.amap.com/api/webservice/download
- 城市编码获取接口：https://restapi.amap.com/v3/config/district
- 项目地图数据包：`map_data` 目录
- 城市编码使用指南：`city_code_guide.md`
- POI分类使用指南：`map_data/USAGE_GUIDE.md`
- 更多使用示例：`map_data/USAGE_GUIDE.md`
- 地理编码API文档：高德地图官方文档
- 逆地理编码API文档：高德地图官方文档