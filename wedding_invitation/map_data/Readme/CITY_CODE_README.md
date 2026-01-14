# 城市编码表使用说明

## 概述
本项目包含了高德地图的城市编码(citycode)和区域编码(adcode)数据，用于地理编码API中指定查询城市和获取区域信息。所有地图数据功能都集中在 `map_data` 包中，提供统一的接口和便捷的使用方法。

## map_data包架构

### 1. 包结构
```
map_data/                           # 地图数据处理包
├── __init__.py                     # 统一导入接口，提供简化调用方式
├── map_data_utils.py               # 主要的数据管理工具
├── city_code_utils.py              # 城市编码处理工具
├── poi_utils.py                    # POI分类处理工具
├── excel_handler.py                # Excel数据处理工具
├── models.py                       # 数据模型定义
└── Readme/                         # 文档目录
    ├── CITY_CODE_README.md         # 城市编码使用说明
    ├── MAP_DATA_GUIDE.md           # 地图数据使用指南
    ├── USAGE_GUIDE.md              # 使用指南
    ├── city_code_guide.md          # 城市编码指南
    └── sample_city_codes.json      # 城市编码示例数据
```

### 2. 统一导入接口
map_data包提供了统一的导入接口，可通过以下方式使用：
```python
# 统一导入常用功能
from map_data import get_adcode, get_city_code, get_poi_name, search_poi

# 导入管理器类
from map_data import CityCodeManager, POICodeManager, MapDataManager
```

## 功能模块详解

### 1. 城市编码处理 (`city_code_utils`)
城市编码处理工具，提供以下功能：
- 根据城市名称获取城市编码(citycode)
- 根据城市名称获取区域编码(adcode)
- 根据区域编码查询城市信息
- 关键词搜索城市
- 支持模糊匹配和精确匹配

### 2. POI分类处理 (`poi_utils`)
POI(Point of Interest)分类处理工具，提供以下功能：
- 根据POI编码获取POI名称
- 根据POI名称获取POI编码
- POI关键词搜索
- POI类型分类查询

### 3. Excel数据处理 (`excel_handler`)
Excel数据处理工具，用于加载和管理高德地图提供的Excel格式数据：
- 加载城市编码数据
- 加载POI分类数据
- 支持数据导出功能

## 使用方法

### 1. 基本查询
```python
from map_data import get_city_code, get_adcode

# 获取城市编码
beijing_code = get_city_code("北京市")  # 返回: 010
shanghai_code = get_city_code("上海市")  # 返回: 021

# 获取区域编码
beijing_adcode = get_adcode("北京市")  # 返回: 110000
shanghai_adcode = get_adcode("上海市")  # 返回: 310000
```

### 2. 使用城市编码管理器
```python
from map_data.city_code_utils import CityCodeManager

manager = CityCodeManager()

# 搜索包含关键词的城市
results = manager.search_cities_by_keyword("北京")

# 获取特定区域编码的城市信息
city_info = manager.get_city_info_by_adcode("110105")  # 朝阳区信息

# 获取城市编码
city_code = manager.get_citycode_by_name("上海市")
```

### 3. 使用POI分类管理器
```python
from map_data.poi_utils import POICodeManager

poi_manager = POICodeManager()

# 获取POI信息
poi_name = poi_manager.get_poi_name_by_code("110100")  # 餐饮服务
poi_code = poi_manager.get_poi_code_by_name("餐饮服务")

# 搜索POI
restaurants = poi_manager.search_poi_by_keyword("餐饮")
```

### 4. 在地理编码API中使用
```python
from invitation.views import geocode_address
from map_data import get_adcode

# 使用城市编码进行地理编码
city_name = "北京市"
adcode = get_adcode(city_name)
result = geocode_address(
    address="北京市朝阳区阜通东大街6号",
    city=adcode,  # 使用adcode参数指定查询城市
    api_key=settings.AMAP_WEB_SERVICE_KEY
)
```

### 5. 与婚礼邀请系统集成
```python
from map_data import get_adcode
from invitation.views import geocode_address

def process_wedding_location(wedding_address, city_name):
    # 获取城市编码以提高地理编码精度
    city_adcode = get_adcode(city_name)
    
    # 进行地理编码
    geocoding_result = geocode_address(
        address=wedding_address,
        city=city_adcode,
        api_key=settings.AMAP_WEB_SERVICE_KEY
    )
    
    if geocoding_result:
        # 使用获取到的坐标初始化地图
        map_config = {
            'center_lat': geocoding_result['latitude'],
            'center_lng': geocoding_result['longitude'],
            'confidence': geocoding_result['confidence'],
            'geocoding_details': geocoding_result
        }
        return map_config
    else:
        # 地理编码失败时返回默认配置
        return {
            'center_lat': 39.90923,  # 天安门坐标
            'center_lng': 116.397428,
            'confidence': 0,
            'geocoding_details': {}
        }
```

### 6. 高级功能使用
```python
from map_data.map_data_utils import MapDataManager

# 使用自定义数据目录
manager = MapDataManager(data_dir="/path/to/custom/data")

# 获取数据模型
from map_data.models import CityInfo, POICategory

# 创建城市信息对象
city = CityInfo(
    name="北京市",
    adcode="110000",
    citycode="010",
    center="116.407170,39.904623",
    level="province"
)
```

## 数据源

### 1. 城市编码数据
- **来源**: `map_files/AMap_adcode_citycode/AMap_adcode_citycode.xlsx`
- **包含**: 中国各省市县的adcode和citycode对照表
- **格式**: Excel文件，包含城市名称、区域编码、城市编码等信息

### 2. POI分类数据
- **来源**: `map_files/Amap_poicode/高德POI分类与编码（中英文）_V1.06_20230208.xlsx`
- **包含**: 高德地图POI分类与编码对照表
- **格式**: Excel文件，包含POI编码、中文名称、英文名称等信息

## 性能优化

### 1. 缓存机制
- 系统内置缓存机制，避免重复查询
- 首次加载后会在内存中缓存数据
- 后续查询直接从缓存获取，提高性能

### 2. 数据预加载
- 数据在首次使用时自动加载
- 支持异步数据加载
- 提供数据加载状态监控

## 数据更新
如果您有完整版的城市编码表，可以将其保存为以下文件：
- `map_files/AMap_adcode_citycode/` - 完整城市编码表
- `map_files/Amap_poicode/` - POI分类数据
- 或者使用自定义数据目录进行配置

## 注意事项
1. 城市编码(citycode)主要用于电话区号，也用于API中的城市指定
2. 区域编码(adcode)是行政区划代码，用于精确的地理区域识别
3. 在地理编码API中，city参数可以接受城市中文、中文全拼、citycode或adcode
4. 建议使用adcode以获得最精确的地理编码结果
5. 所有地图数据功能都已整合到 `map_data` 包中，便于维护和管理
6. 数据文件路径默认为 `map_files` 目录，可通过配置更改
7. 包含缓存机制，首次加载可能较慢，后续使用会显著提升性能
8. 支持中文城市名称和英文POI名称的搜索

## 最佳实践
1. **优先使用统一导入接口**：推荐使用 `from map_data import ...` 方式导入功能
2. **利用缓存机制**：系统内置缓存机制，避免重复API调用
3. **处理异常情况**：始终检查返回值，处理可能的None情况
4. **数据更新**：定期更新Excel数据文件以获取最新的编码信息

## 参考资源
- [高德开放平台城市编码表](https://lbs.amap.com/api/webservice/download)
- [高德地理编码API文档](https://lbs.amap.com/api/webservice/guide/api/georegeo)
- [项目地图数据包](../..) - `map_data` 目录
- [城市编码使用指南](./city_code_guide.md)
- [地图数据使用指南](./MAP_DATA_GUIDE.md)