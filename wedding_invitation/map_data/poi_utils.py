"""
POI分类处理工具
用于处理高德地图POI分类编码相关功能
提供POI分类的查询、搜索、管理等功能，支持编码与名称之间的双向转换
"""

import os
from typing import Dict, List, Optional
from .map_data_utils import map_data_manager
from .models import POICategory


class POICodeManager:
    """
    POI分类编码管理器
    
    管理高德地图POI分类编码数据，提供POI编码与名称之间的查询、
    搜索和管理功能，支持分类数据的高效检索和操作。
    """
    
    def __init__(self, data_dir: str = "map_files/Amap_poicode"):
        """
        初始化POI分类编码管理器
        
        从全局地图数据管理器中获取POI分类数据，建立本地引用。
        该管理器依赖于map_data_utils模块提供的数据结构。
        
        Args:
            data_dir: 存放POI分类数据的目录，默认为'map_files/Amap_poicode'
        """
        # 存放POI分类数据的目录路径
        self.data_dir = data_dir
        # 引用全局地图数据管理器中的POI编码到名称的映射
        self.poi_codes = map_data_manager.poi_codes
        # 引用全局地图数据管理器中的POI分类对象列表
        self.poi_categories = map_data_manager.poi_categories
    
    def get_poi_name_by_code(self, poi_code: str) -> Optional[str]:
        """
        根据POI编码获取POI名称
            
        通过预先构建的POI编码到名称的映射表，快速查询POI的中文名称。
        该方法委托给全局地图数据管理器处理实际查询逻辑。
            
        Args:
            poi_code: POI编码，用于查询对应的POI名称
            
        Returns:
            POI名称字符串，如果未找到对应的编码则返回None
        """
        # 委托给全局地图数据管理器执行实际的POI名称查询
        return map_data_manager.get_poi_name_by_code(poi_code)
    
    def get_poi_code_by_name(self, poi_name: str) -> Optional[str]:
        """
        根据POI名称获取POI编码
            
        通过遍历POI名称到编码的映射，实现从POI名称到POI编码的反向查询。
        注意：如果存在同名POI分类，只会返回第一个匹配的编码。
            
        Args:
            poi_name: POI名称，用于查询对应的POI编码
            
        Returns:
            POI编码字符串，如果未找到对应的名称则返回None
        """
        # 遍历POI编码到名称的映射，寻找匹配的POI名称
        for code, name in self.poi_codes.items():
            # 检查当前POI名称是否与查询名称匹配
            if name == poi_name:
                # 如果找到匹配项，返回对应的POI编码
                return code
        # 如果遍历完所有POI仍未找到匹配项，返回None
        return None
    
    def search_poi_by_keyword(self, keyword: str) -> List[tuple]:
        """
        根据关键词搜索POI分类
            
        在所有POI编码和名称中进行模糊匹配，返回包含关键词的POI项目。
        支持对POI编码和POI名称的大小写不敏感搜索。
            
        Args:
            keyword: 搜索关键词，可以是POI名称的一部分或编码的一部分
            
        Returns:
            匹配的POI编码和名称的元组列表，格式为[(code, name), ...]
        """
        # 委托给全局地图数据管理器执行实际的POI关键词搜索
        return map_data_manager.search_poi_by_keyword(keyword)
    
    def get_all_poi_categories(self) -> List[str]:
        """
        获取所有POI分类名称
        
        提取所有唯一的POI分类名称，去重后返回列表。
        该方法可用于获取系统支持的全部POI分类种类。
        
        Returns:
            POI分类名称列表，包含所有唯一的POI分类名称
        """
        # 从POI编码到名称的映射中提取所有名称值，使用set去重，然后转换为列表返回
        return list(set(self.poi_codes.values()))
    
    def get_poi_codes_by_category(self, category: str) -> List[str]:
        """
        根据分类名称获取所有对应的POI编码
            
        查找所有包含指定分类名称的POI项，支持模糊匹配。
        返回所有匹配项的POI编码列表。
            
        Args:
            category: POI分类名称，用于搜索匹配的POI编码
            
        Returns:
            匹配的POI编码列表，包含所有符合分类条件的POI编码
        """
        # 初始化结果列表，用于存储匹配的POI编码
        codes = []
        # 遍历所有POI编码到名称的映射项
        for code, name in self.poi_codes.items():
            # 检查分类名称是否存在于POI名称中（忽略大小写）
            if category.lower() in name.lower():
                # 如果匹配，将POI编码添加到结果列表
                codes.append(code)
        # 返回匹配的POI编码列表
        return codes
    
    def get_poi_category_by_code(self, code: str) -> Optional[POICategory]:
        """
        根据编码获取POI分类对象
            
        通过遍历POI分类对象列表，查找指定编码对应的完整POI分类对象。
        返回包含编码、名称、英文名称和父级编码等完整信息的对象。
            
        Args:
            code: POI编码，用于查询对应的POI分类对象
            
        Returns:
            POICategory对象，如果未找到对应的编码则返回None
        """
        # 遍历所有POI分类对象，寻找匹配的编码
        for poi in self.poi_categories:
            # 检查当前POI对象的编码是否与查询编码匹配
            if poi.code == code:
                # 如果找到匹配项，返回完整的POI分类对象
                return poi
        # 如果遍历完所有POI分类仍未找到匹配项，返回None
        return None


# 创建全局POI编码管理器实例，用于在整个应用中共享POI数据
poi_manager = POICodeManager()


def get_poi_name(poi_code: str) -> Optional[str]:
    """
    获取POI名称的便捷函数
    
    提供全局访问接口，方便其他模块根据POI编码获取POI名称。
    该函数封装了对POICodeManager实例的调用，简化了外部使用方式。
    
    Args:
        poi_code: POI编码，用于查询对应的POI名称
    
    Returns:
        POI名称字符串，如果未找到则返回None
    """
    # 调用全局POI编码管理器实例的POI名称查询方法
    return poi_manager.get_poi_name_by_code(poi_code)


def get_poi_code(poi_name: str) -> Optional[str]:
    """
    获取POI编码的便捷函数
    
    提供全局访问接口，方便其他模块根据POI名称获取POI编码。
    该函数封装了对POICodeManager实例的调用，简化了外部使用方式。
    
    Args:
        poi_name: POI名称，用于查询对应的POI编码
    
    Returns:
        POI编码字符串，如果未找到则返回None
    """
    # 调用全局POI编码管理器实例的POI编码查询方法
    return poi_manager.get_poi_code_by_name(poi_name)


def search_poi(keyword: str) -> List[tuple]:
    """
    搜索POI的便捷函数
    
    提供全局访问接口，方便其他模块根据关键词搜索POI分类。
    该函数封装了对POICodeManager实例的调用，简化了外部使用方式。
    
    Args:
        keyword: 搜索关键词，可以是POI名称或编码的一部分
    
    Returns:
        匹配的POI编码和名称的元组列表，格式为[(code, name), ...]
    """
    # 调用全局POI编码管理器实例的POI关键词搜索方法
    return poi_manager.search_poi_by_keyword(keyword)


if __name__ == "__main__":
    # 示例用法
    print("POI分类工具示例:")
    print("POI分类数量:", len(map_data_manager.poi_codes))
    
    # 搜索包含"餐饮"的POI
    food_pois = search_poi("餐饮")
    print("餐饮类POI示例:", food_pois[:5])  # 显示前5个结果