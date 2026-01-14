"""
地图数据模型
定义与地图相关的数据结构
包括城市信息、区域信息、POI分类、地理编码结果等数据类
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class CityInfo:
    """
    城市信息数据类
    
    表示一个城市的完整信息，包括城市名称、区域编码、城市编码、中心坐标等。
    同时包含该城市下辖的所有区域信息列表。
    """
    # 城市名称，例如'北京市'、'上海市'等
    name: str
    # 区域编码，高德地图中唯一的区域标识符，如'110000'代表北京市
    adcode: str
    # 城市编码，高德地图中城市级别的标识符
    citycode: str
    # 城市中心坐标，格式为'经度,纬度'
    center: str
    # 城市等级，如'city'、'province'等
    level: str
    # 该城市下辖的区域信息列表，可能包含多个DistrictInfo对象
    districts: List['DistrictInfo'] = None
    
    def __post_init__(self):
        # 如果districts未初始化，则创建空列表
        if self.districts is None:
            self.districts = []


@dataclass
class DistrictInfo:
    """
    区域信息数据类
    
    表示一个行政区域的信息，通常隶属于某个城市，包含区域名称、
    区域编码、城市编码、中心坐标等信息。
    """
    # 区域名称，例如'朝阳区'、'浦东新区'等
    name: str
    # 区域编码，高德地图中唯一的区域标识符，如'110105'代表北京市朝阳区
    adcode: str
    # 城市编码，所属城市的编码
    citycode: str
    # 区域中心坐标，格式为'经度,纬度'
    center: str
    # 区域等级，如'district'、'county'等
    level: str


@dataclass
class POICategory:
    """
    POI分类数据类
    
    表示兴趣点(Point of Interest)的分类信息，包含POI编码、中文名称、
    英文名称和父级分类编码，用于建立POI分类的层级结构。
    """
    # POI分类编码，高德地图中唯一的分类标识符，如'110100'代表风景名胜
    code: str
    # POI分类中文名称，如'风景名胜'、'餐饮服务'等
    name: str
    # POI分类英文名称，可选字段，如'Scenic Spot'、'Food Service'等
    english_name: Optional[str] = None
    # 父级POI分类编码，用于构建POI分类的层级结构，可选字段
    parent_code: Optional[str] = None


@dataclass
class GeocodingResult:
    """
    地理编码结果数据类
    
    表示地理编码API调用的结果，包含经纬度坐标、格式化地址、
    行政区划信息、置信度等详细信息。
    """
    # 经度，表示地理位置的东西方向坐标
    longitude: float
    # 纬度，表示地理位置的南北方向坐标
    latitude: float
    # 格式化地址，如'北京市朝阳区望京街道望京SOHO'
    formatted_address: str
    # 国家名称
    country: str
    # 省份/直辖市名称
    province: str
    # 城市名称
    city: str
    # 区县名称
    district: str
    # 街道名称
    street: str
    # 门牌号
    number: str
    # 区域编码
    adcode: str
    # 地址等级
    level: str
    # 地理编码结果的置信度，数值越高表示结果越可靠
    confidence: int
    # 商圈列表，包含该位置附近的商业区域
    business_area: List[str]
    # 小区/社区信息
    neighborhood: Dict


@dataclass
class ReverseGeocodingResult:
    """
    逆地理编码结果数据类
    
    表示逆地理编码API调用的结果，将经纬度坐标转换为详细的地址信息，
    包括行政区划、道路、POI等周边信息。
    """
    # 格式化地址，如'北京市朝阳区望京街道望京SOHO'
    formatted_address: str
    # 国家名称
    country: str
    # 省份/直辖市名称
    province: str
    # 城市名称
    city: str
    # 区县名称
    district: str
    # 乡镇/街道名称
    township: str
    # 社区/小区名称
    neighborhood: str
    # 建筑物名称
    building: str
    # 街道号码
    street_number: str
    # 街道名称
    street: str
    # 附近的POI列表，包含周围兴趣点信息
    poi_list: List[Dict]
    # 附近的道路列表，包含周围道路信息
    road_list: List[Dict]