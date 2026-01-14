# 高德地图城市编码表使用指南

## 说明
此文档介绍项目中使用的高德地图城市编码表功能。所有地图数据处理功能都集中在 `map_data` 包中，包括城市编码(citycode)和区域编码(adcode)对照表、POI分类编码等功能。本文档详细介绍了API使用方法和错误处理机制。

## 城市编码表简介
高德地图API中的城市编码(citycode)和区域编码(adcode)是重要的地理信息标识符：

- **citycode**：城市编码，用于标识特定城市，如北京为010，上海为021
- **adcode**：区域编码，用于标识行政区域，如北京市为110000，上海市为310000

## 项目结构
```
map_data/                           # 地图数据处理包
├── __init__.py                     # 包初始化文件，提供统一导入接口
├── map_data_utils.py               # 主要数据管理工具
├── city_code_utils.py              # 城市编码处理工具
├── poi_utils.py                    # POI分类处理工具
├── excel_handler.py                # Excel数据处理工具
├── models.py                       # 数据模型定义
├── Readme/                         # 文档目录
│   ├── CITY_CODE_README.md         # 城市编码使用说明
│   ├── MAP_DATA_GUIDE.md           # 地图数据使用指南
│   ├── USAGE_GUIDE.md              # 使用指南
│   ├── city_code_guide.md          # 城市编码指南（此文件）
│   └── sample_city_codes.json      # 城市编码示例数据
└── __pycache__/                    # Python缓存目录
```

## 使用场景
- 地理编码API中指定查询城市
- 逆地理编码API中获取区域信息
- 地图展示时的区域定位
- POI搜索和分类过滤
- 婚礼邀请系统的地点精确化

## 使用方法

### 1. 基本导入（推荐）
```python
# 统一导入接口
from map_data import get_adcode, get_city_code, get_poi_name, search_poi

# 获取北京市的编码
adcode = get_adcode("北京市")      # 返回区域编码
citycode = get_city_code("北京市") # 返回城市编码

# 获取POI信息
poi_name = get_poi_name("110100")  # 根据编码获取POI名称
poi_results = search_poi("餐饮")   # 搜索POI分类
```

### 2. 使用管理器类
```python
from map_data.city_code_utils import CityCodeManager
from map_data.poi_utils import POICodeManager

# 城市编码管理器
city_manager = CityCodeManager()
city_code = city_manager.get_citycode_by_name("北京市")
adcode = city_manager.get_adcode_by_name("北京市")
cities = city_manager.search_cities_by_keyword("北京")

# POI编码管理器
poi_manager = POICodeManager()
poi_name = poi_manager.get_poi_name_by_code("110100")
poi_codes = poi_manager.search_poi_by_keyword("餐饮")
```

### 3. 与地理编码API集成
```python
from invitation.views import geocode_address, reverse_geocode
from map_data import get_adcode

# 地理编码 - 使用城市编码
city_name = "北京市"
adcode = get_adcode(city_name)
result = geocode_address(
    address="北京市朝阳区阜通东大街6号",
    city=adcode,  # 使用adcode参数指定查询城市
    api_key=settings.AMAP_API_KEY
)

# 逆地理编码 - 使用POI类型
result = reverse_geocode(
    lat=39.997213,
    lng=116.481938,
    api_key=settings.AMAP_API_KEY,
    poitype="商务写字楼",  # 使用POI类型过滤
    extensions='all'
)
```

### 4. Excel数据处理
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

## 数据源
- **城市编码数据**：`map_files/AMap_adcode_citycode/AMap_adcode_citycode.xlsx`
- **POI分类数据**：`map_files/Amap_poicode/高德POI分类与编码（中英文）_V1.06_20230208.xlsx`

## API使用示例

### 1. 城市编码查询示例
```python
from map_data import get_adcode, get_city_code

# 查询城市编码
beijing_adcode = get_adcode("北京市")
shanghai_code = get_city_code("上海市")

# 处理查询结果
if beijing_adcode:
    print(f"北京市的区域编码是: {beijing_adcode}")
else:
    print("未找到北京市的区域编码")

if shanghai_code:
    print(f"上海市的城市编码是: {shanghai_code}")
else:
    print("未找到上海市的城市编码")
```

### 2. 多种查询方式示例
```python
from map_data.city_code_utils import CityCodeManager

# 使用管理器进行查询
manager = CityCodeManager()

# 精确查询
adcode = manager.get_adcode_by_name("北京市")
citycode = manager.get_citycode_by_name("北京市")

# 模糊搜索
cities = manager.search_cities_by_keyword("北京")
print(f"包含'北京'的地区: {cities}")

# 根据adcode查询城市信息
city_info = manager.get_city_info_by_adcode("110105")  # 朝阳区
print(f"朝阳区信息: {city_info}")
```

### 3. POI分类查询示例
```python
from map_data import search_poi, get_poi_name

# 搜索POI
restaurants = search_poi("餐饮")
print(f"餐饮类POI: {restaurants}")

# 根据编码获取POI名称
hotel_name = get_poi_name("120000")  # 住宿服务
print(f"POI编码120000的名称: {hotel_name}")
```

## 错误处理

### 1. 基础错误处理
```python
from map_data import get_adcode, get_city_code

# 安全查询函数
def safe_get_city_code(city_name):
    try:
        city_code = get_city_code(city_name)
        if city_code:
            return city_code
        else:
            print(f"未找到城市 '{city_name}' 的编码")
            return None
    except Exception as e:
        print(f"查询城市编码时发生错误: {e}
        return None

# 使用安全查询
result = safe_get_city_code("虚构市")
if result is None:
    print("查询失败，使用默认值")
```

### 2. 完整的错误处理示例
```python
from map_data import get_adcode
from invitation.views import geocode_address
from django.conf import settings

def process_address_with_error_handling(address, city_name=None):
    """处理地址的完整错误处理示例"""
    try:
        # 如果提供了城市名称，使用城市编码提高精度
        city_param = None
        if city_name:
            city_adcode = get_adcode(city_name)
            if city_adcode:
                city_param = city_adcode
                print(f"使用城市编码: {city_adcode}")
            else:
                print(f"未找到城市 '{city_name}' 的编码，将使用地址本身")
        
        # 进行地理编码
        result = geocode_address(
            address=address,
            city=city_param,
            api_key=settings.AMAP_API_KEY
        )
        
        if result:
            print(f"地理编码成功: ({result['longitude']}, {result['latitude']})")
            print(f"置信度: {result['confidence']}/5")
            return result
        else:
            print("地理编码失败")
            return None
            
    except Exception as e:
        print(f"地理编码过程中发生错误: {e}")
        return None

# 使用示例
address_result = process_address_with_error_handling(
    "北京市朝阳区阜通东大街6号", 
    "北京市"
)
```

### 3. 数据验证和回退机制
```python
from map_data import get_adcode

def get_city_code_with_fallback(city_name):
    """带回退机制的城市编码查询"""
    # 首先尝试精确匹配
    adcode = get_adcode(city_name)
    if adcode:
        return adcode
    
    # 如果精确匹配失败，尝试模糊搜索
    from map_data.city_code_utils import CityCodeManager
    manager = CityCodeManager()
    cities = manager.search_cities_by_keyword(city_name)
    
    if cities:
        # 如果找到匹配项，使用第一个结果
        first_match = cities[0]
        fallback_adcode = get_adcode(first_match['name'])
        if fallback_adcode:
            print(f"使用模糊匹配结果: {first_match['name']}")
            return fallback_adcode
    
    print(f"无法找到城市 '{city_name}' 的编码")
    return None

# 使用回退机制
result = get_city_code_with_fallback("上海")
if result:
    print(f"找到编码: {result}")
else:
    print("最终回退到默认值")
```

### 4. 异常日志记录
```python
import logging
from map_data import get_adcode

logger = logging.getLogger(__name__)

def log_city_code_query(city_name):
    """带日志记录的城市编码查询"""
    logger.info(f"开始查询城市编码: {city_name}")
    
    try:
        adcode = get_adcode(city_name)
        
        if adcode:
            logger.info(f"成功查询到城市编码: {city_name} -> {adcode}")
            return adcode
        else:
            logger.warning(f"未找到城市编码: {city_name}")
            return None
            
    except Exception as e:
        logger.error(f"查询城市编码时发生异常: {city_name}, 错误: {str(e)}")
        return None

# 使用带日志的查询
result = log_city_code_query("北京市")
```

## 高级功能

### 1. 自定义数据源
```python
from map_data.map_data_utils import MapDataManager

# 使用自定义数据目录
custom_manager = MapDataManager(data_dir="/path/to/custom/data")
```

### 2. 数据模型使用
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

## 错误类型和解决方案

### 1. 常见错误类型
- **ValueError**: 数据格式错误
- **KeyError**: 数据键不存在
- **TypeError**: 数据类型错误
- **FileNotFoundError**: 数据文件不存在

### 2. 解决方案
```python
import os
from map_data import get_adcode

def robust_city_code_lookup(city_name):
    """健壮的城市编码查询"""
    # 验证输入
    if not isinstance(city_name, str):
        raise TypeError("城市名称必须是字符串")
    
    if not city_name.strip():
        raise ValueError("城市名称不能为空")
    
    # 清理输入
    clean_city_name = city_name.strip()
    
    # 执行查询
    try:
        result = get_adcode(clean_city_name)
        return result
    except KeyError as e:
        print(f"数据键错误: {e}")
        return None
    except Exception as e:
        print(f"查询过程中发生错误: {e}")
        return None

# 使用健壮查询
try:
    result = robust_city_code_lookup("北京市")
    if result:
        print(f"查询成功: {result}")
    else:
        print("查询失败")
except (TypeError, ValueError) as e:
    print(f"输入错误: {e}")
```

## 最佳实践

1. **优先使用统一导入接口**：推荐使用 `from map_data import ...` 方式导入功能
2. **利用缓存机制**：系统内置缓存机制，避免重复API调用
3. **处理异常情况**：始终检查返回值，处理可能的None情况
4. **数据更新**：定期更新Excel数据文件以获取最新的编码信息
5. **错误处理**：实现适当的错误处理和回退机制
6. **日志记录**：记录重要的查询和错误信息
7. **输入验证**：验证输入参数的有效性
8. **资源清理**：适当处理和清理不再需要的资源

## 参考资料
- 高德开放平台城市编码表：https://lbs.amap.com/api/webservice/download
- 城市编码获取接口：https://restapi.amap.com/v3/config/district
- 项目地图数据包：`map_data` 目录
- 更多使用示例：`map_data/USAGE_GUIDE.md`
- 错误处理最佳实践：Python官方文档