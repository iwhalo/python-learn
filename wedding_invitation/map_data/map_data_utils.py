"""
地图数据处理工具
用于处理高德地图城市编码(citycode)、区域编码(adcode)和POI分类编码
提供高效的数据管理和查询功能，支持城市信息和兴趣点(POI)的快速检索
"""

# 导入标准库模块
import json  # 用于JSON数据的序列化和反序列化，便于数据交换和存储
import os    # 用于操作系统相关功能，如路径操作和文件系统交互
import logging  # 用于记录日志信息，便于调试和监控系统运行状态
from typing import Dict, List, Optional, Tuple  # 用于类型提示，增强代码可读性和IDE支持

# 导入第三方库
import pandas as pd  # 用于数据处理和分析，提供高效的DataFrame数据结构

# 导入项目内部模块
from .models import POICategory, CityInfo  # 导入数据模型，定义POI和城市信息的数据结构
from .excel_handler import excel_handler  # 导入Excel处理器，用于读取和解析Excel格式的地图数据

# 配置日志记录器
logger = logging.getLogger(__name__)  # 获取当前模块的日志记录器实例，用于记录操作日志


class MapDataManager:
    """
    地图数据管理器
    
    负责加载、管理和提供对高德地图数据的访问，包括POI分类和城市编码数据。
    提供高效的数据查询接口，支持按编码、名称等方式快速检索城市和POI信息。
    """
    
    def __init__(self, data_dir: str = "map_files"):
        """
        初始化地图数据管理器
        
        该构造函数设置数据目录路径，初始化内部数据结构，并立即加载地图数据
        以便后续的查询操作。数据加载完成后，可以通过各种方法查询POI和城市信息。
        
        Args:
            data_dir: 存放地图数据的目录，默认为'map_files'
        """
        # 存储地图数据的目录路径，用于查找POI和城市编码的Excel文件
        self.data_dir = data_dir
        # POI编码到名称的映射字典，用于快速查询POI名称
        self.poi_codes = {}
        # 城市编码的多重映射字典，包含adcode、citycode和城市名称之间的双向映射
        self.city_codes = {}
        # 存储所有POI分类对象的列表
        self.poi_categories = []
        # 存储所有城市信息对象的列表
        self.cities = []
        
        # 立即加载地图数据，构建内存中的数据结构
        self.load_map_data()
    
    def load_map_data(self):
        """
        加载地图数据
        
        从Excel文件中加载POI分类数据和城市编码数据，并构建内存中的映射表
        以实现快速的数据查询。该方法会在初始化时自动调用，也可以手动调用
        以重新加载数据。
        """
        # 记录数据加载开始，便于跟踪系统运行状态
        logger.info("开始加载地图数据")
        
        # 加载POI分类编码数据，这是地图功能的重要组成部分
        try:
            # 记录开始加载POI数据的日志
            logger.debug("开始加载POI数据")
            # 调用Excel处理器加载POI数据
            self.poi_categories = excel_handler.load_poi_data()
            # 记录POI数据加载完成的日志
            logger.info(f"POI数据加载完成 - 数量: {len(self.poi_categories)}")
            
            # 创建POI编码到名称的映射，以实现O(1)时间复杂度的快速查询
            self.poi_codes = {poi.code: poi.name for poi in self.poi_categories}
            # 记录POI编码映射创建完成的日志
            logger.debug(f"POI编码映射创建完成 - 数量: {len(self.poi_codes)}")
        except Exception as e:
            # 捕获POI数据加载异常并记录错误日志
            logger.error(f"加载POI数据失败: {e}")
            # 打印错误信息到控制台
            print(f"加载POI数据失败: {e}")
        
        # 加载城市编码数据，用于地理编码和逆地理编码功能
        try:
            # 记录开始加载城市编码数据的日志
            logger.debug("开始加载城市编码数据")
            # 调用Excel处理器加载城市数据
            self.cities = excel_handler.load_city_data()
            # 记录城市编码数据加载完成的日志
            logger.info(f"城市编码数据加载完成 - 数量: {len(self.cities)}")
            
            # 创建城市编码映射，包括adcode、citycode和城市名称之间的双向映射
            logger.debug("开始创建城市编码映射")
            self.city_codes = {
                # adcode到城市名称的映射，用于根据区域编码查询城市名称
                'adcode_to_name': {city.adcode: city.name for city in self.cities},
                # citycode到城市名称的映射，用于根据城市编码查询城市名称
                'citycode_to_name': {city.citycode: city.name for city in self.cities},
                # 城市名称到adcode的映射，用于根据城市名称查询区域编码
                'name_to_adcode': {city.name: city.adcode for city in self.cities},
                # 城市名称到citycode的映射，用于根据城市名称查询城市编码
                'name_to_citycode': {city.name: city.citycode for city in self.cities}
            }
            # 记录城市编码映射创建完成的日志
            logger.debug(f"城市编码映射创建完成 - 包含 {len(self.cities)} 个城市")
        except Exception as e:
            # 捕获城市数据加载异常并记录错误日志
            logger.error(f"加载城市编码数据失败: {e}")
            # 打印错误信息到控制台
            print(f"加载城市编码数据失败: {e}")
        
        # 记录数据加载完成，表明系统已准备好处理地图相关的请求
        logger.info("地图数据加载完成")
    
    def get_poi_name_by_code(self, poi_code: str) -> Optional[str]:
        """
        根据POI编码获取POI名称
            
        通过预先构建的POI编码到名称的映射表，快速查询POI的中文名称。
        该方法的时间复杂度为O(1)，适用于高频查询场景。
            
        Args:
            poi_code: POI编码，通常是数字或字母组成的字符串
            
        Returns:
            POI名称，如果未找到对应的编码则返回None
        """
        # 记录POI编码查询的调试日志，便于追踪查询过程
        logger.debug(f"根据POI编码查询名称 - 编码: {poi_code}")
        # 从预构建的POI编码映射字典中获取对应的POI名称
        result = self.poi_codes.get(poi_code)
        # 检查查询结果并记录相应日志
        if result:
            # 查询成功时记录信息日志
            logger.info(f"成功查询到POI名称 - 编码: {poi_code}, 名称: {result}")
        else:
            # 查询失败时记录警告日志
            logger.warning(f"未找到POI编码对应的名称 - 编码: {poi_code}")
        # 返回查询结果
        return result
    
    def get_adcode_by_city_name(self, city_name: str) -> Optional[str]:
        """
        根据城市名称获取区域编码
            
        通过预先构建的城市名称到区域编码(adcode)的映射表，快速查询城市的区域编码。
        区域编码是高德地图API中的重要参数，用于地理编码和逆地理编码服务。
            
        Args:
            city_name: 城市名称，例如'北京市'、'上海市'等
            
        Returns:
            区域编码字符串，如果未找到对应的名称则返回None
        """
        # 记录城市名称查询adcode的调试日志，便于追踪查询过程
        logger.debug(f"根据城市名称查询区域编码 - 城市名称: {city_name}")
        # 检查城市编码映射字典中是否存在name_to_adcode映射
        if 'name_to_adcode' in self.city_codes:
            # 从预构建的映射表中获取城市名称对应的区域编码
            result = self.city_codes['name_to_adcode'].get(city_name)
            # 检查查询结果并记录相应日志
            if result:
                # 查询成功时记录信息日志
                logger.info(f"成功查询到区域编码 - 城市名称: {city_name}, adcode: {result}")
            else:
                # 城市名称未找到时记录警告日志
                logger.warning(f"未找到城市名称对应的区域编码 - 城市名称: {city_name}")
            # 返回查询结果
            return result
        # 如果映射数据不存在，记录警告日志并返回None
        logger.warning(f"城市编码映射数据缺失 - 城市名称: {city_name}")
        return None
    
    def get_citycode_by_city_name(self, city_name: str) -> Optional[str]:
        """
        根据城市名称获取城市编码
            
        通过预先构建的城市名称到城市编码(citycode)的映射表，快速查询城市的编码。
        城市编码是高德地图API中的另一种重要参数，通常用于城市级别的地理服务。
            
        Args:
            city_name: 城市名称，例如'北京市'、'上海市'等
            
        Returns:
            城市编码字符串，如果未找到对应的名称则返回None
        """
        # 记录城市名称查询citycode的调试日志，便于追踪查询过程
        logger.debug(f"根据城市名称查询城市编码 - 城市名称: {city_name}")
        # 检查城市编码映射字典中是否存在name_to_citycode映射
        if 'name_to_citycode' in self.city_codes:
            # 从预构建的映射表中获取城市名称对应的城市编码
            result = self.city_codes['name_to_citycode'].get(city_name)
            # 检查查询结果并记录相应日志
            if result:
                # 查询成功时记录信息日志
                logger.info(f"成功查询到城市编码 - 城市名称: {city_name}, citycode: {result}")
            else:
                # 城市名称未找到时记录警告日志
                logger.warning(f"未找到城市名称对应的城市编码 - 城市名称: {city_name}")
            # 返回查询结果
            return result
        # 如果映射数据不存在，记录警告日志并返回None
        logger.warning(f"城市编码映射数据缺失 - 城市名称: {city_name}")
        return None
    
    def get_city_name_by_adcode(self, adcode: str) -> Optional[str]:
        """
        根据区域编码获取城市名称
            
        通过预先构建的区域编码(adcode)到城市名称的映射表，实现从区域编码到城市名称的反向查询。
        该功能常用于地理编码API返回结果的解析和展示。
            
        Args:
            adcode: 区域编码，由数字组成的字符串，如'110000'代表北京市
            
        Returns:
            城市名称字符串，如果未找到对应的编码则返回None
        """
        # 记录区域编码查询城市名称的调试日志，便于追踪查询过程
        logger.debug(f"根据区域编码查询城市名称 - adcode: {adcode}")
        # 检查城市编码映射字典中是否存在adcode_to_name映射
        if 'adcode_to_name' in self.city_codes:
            # 从预构建的映射表中获取区域编码对应的城市名称
            result = self.city_codes['adcode_to_name'].get(adcode)
            # 检查查询结果并记录相应日志
            if result:
                # 查询成功时记录信息日志
                logger.info(f"成功查询到城市名称 - adcode: {adcode}, 城市名称: {result}")
            else:
                # 区域编码未找到时记录警告日志
                logger.warning(f"未找到区域编码对应的城市名称 - adcode: {adcode}")
            # 返回查询结果
            return result
        # 如果映射数据不存在，记录警告日志并返回None
        logger.warning(f"城市编码映射数据缺失 - adcode: {adcode}")
        return None
    
    def get_city_name_by_citycode(self, citycode: str) -> Optional[str]:
        """
        根据城市编码获取城市名称
            
        通过预先构建的城市编码(citycode)到城市名称的映射表，实现从城市编码到城市名称的反向查询。
        该功能常用于城市级别地理服务的响应数据解析。
            
        Args:
            citycode: 城市编码，由数字组成的字符串，用于标识特定城市
            
        Returns:
            城市名称字符串，如果未找到对应的编码则返回None
        """
        # 记录城市编码查询城市名称的调试日志，便于追踪查询过程
        logger.debug(f"根据城市编码查询城市名称 - citycode: {citycode}")
        # 检查城市编码映射字典中是否存在citycode_to_name映射
        if 'citycode_to_name' in self.city_codes:
            # 从预构建的映射表中获取城市编码对应的城市名称
            result = self.city_codes['citycode_to_name'].get(citycode)
            # 检查查询结果并记录相应日志
            if result:
                # 查询成功时记录信息日志
                logger.info(f"成功查询到城市名称 - citycode: {citycode}, 城市名称: {result}")
            else:
                # 城市编码未找到时记录警告日志
                logger.warning(f"未找到城市编码对应的城市名称 - citycode: {citycode}")
            # 返回查询结果
            return result
        # 如果映射数据不存在，记录警告日志并返回None
        logger.warning(f"城市编码映射数据缺失 - citycode: {citycode}")
        return None
    
    def search_poi_by_keyword(self, keyword: str) -> List[Tuple[str, str]]:
        """
        根据关键词搜索POI
            
        在所有POI编码和名称中进行模糊匹配，返回包含关键词的POI项目。
        支持对POI编码和POI名称的大小写不敏感搜索。
            
        Args:
            keyword: 搜索关键词，可以是POI名称的一部分或编码的一部分
            
        Returns:
            匹配的POI编码和名称的元组列表，格式为[(code, name), ...]
        """
        # 记录POI关键词搜索的调试日志，便于追踪搜索过程
        logger.debug(f"根据关键词搜索POI - 关键词: {keyword}")
        # 初始化结果列表，用于存储匹配的POI编码和名称
        results = []
        # 遍历所有POI编码和名称的映射项
        for code, name in self.poi_codes.items():
            # 检查关键词是否存在于POI编码或名称中（忽略大小写）
            if keyword.lower() in code.lower() or keyword.lower() in name.lower():
                # 如果匹配，则将POI编码和名称添加到结果列表
                results.append((code, name))
        # 记录POI搜索完成的信息日志
        logger.info(f"POI搜索完成 - 关键词: {keyword}, 匹配数量: {len(results)}")
        # 返回匹配的POI结果列表
        return results
    
    def search_city_by_keyword(self, keyword: str) -> List[Dict]:
        """
        根据关键词搜索城市
            
        在城市名称和区域编码中进行模糊匹配，返回包含关键词的城市信息。
        搜索结果包含城市的adcode、citycode和名称等完整信息。
            
        Args:
            keyword: 搜索关键词，可以是城市名称的一部分或编码的一部分
            
        Returns:
            匹配的城市信息列表，每个元素包含adcode、citycode和name字段
        """
        # 初始化结果列表，用于存储匹配的城市信息
        results = []
        # 检查城市编码映射数据是否存在
        if 'adcode_to_name' in self.city_codes:
            # 遍历所有区域编码和城市名称的映射项
            for adcode, name in self.city_codes['adcode_to_name'].items():
                # 检查关键词是否存在于城市名称或区域编码中
                if keyword in name or keyword in str(adcode):
                    # 构建城市信息字典，包含adcode、citycode和名称
                    city_info = {
                        # 区域编码
                        'adcode': adcode,
                        # 从城市名称获取对应的城市编码
                        'citycode': self.city_codes['name_to_citycode'].get(name),
                        # 城市名称
                        'name': name
                    }
                    # 将城市信息添加到结果列表
                    results.append(city_info)
        # 返回匹配的城市信息列表
        return results


# 创建全局地图数据管理器实例，用于在整个应用中共享地图数据
map_data_manager = MapDataManager()


def get_poi_name(code: str) -> Optional[str]:
    """
    获取POI名称的便捷函数
    
    提供全局访问接口，方便其他模块获取POI名称信息。
    该函数封装了对MapDataManager实例的调用，简化了外部使用方式。
    
    Args:
        code: POI编码，用于查询对应的POI名称
    
    Returns:
        POI名称字符串，如果未找到则返回None
    """
    # 调用全局地图数据管理器实例的POI名称查询方法
    return map_data_manager.get_poi_name_by_code(code)


def get_adcode(city_name: str) -> Optional[str]:
    """
    获取区域编码的便捷函数
    
    提供全局访问接口，方便其他模块根据城市名称获取区域编码。
    该函数封装了对MapDataManager实例的调用，简化了外部使用方式。
    
    Args:
        city_name: 城市名称，例如'北京市'、'上海市'等
    
    Returns:
        区域编码字符串，如果未找到则返回None
    """
    # 调用全局地图数据管理器实例的区域编码查询方法
    return map_data_manager.get_adcode_by_city_name(city_name)


def get_citycode(city_name: str) -> Optional[str]:
    """
    获取城市编码的便捷函数
    
    提供全局访问接口，方便其他模块根据城市名称获取城市编码。
    该函数封装了对MapDataManager实例的调用，简化了外部使用方式。
    
    Args:
        city_name: 城市名称，例如'北京市'、'上海市'等
    
    Returns:
        城市编码字符串，如果未找到则返回None
    """
    # 调用全局地图数据管理器实例的城市编码查询方法
    return map_data_manager.get_citycode_by_city_name(city_name)


def get_city_by_adcode(adcode: str) -> Optional[str]:
    """
    根据区域编码获取城市名称的便捷函数
    
    提供全局访问接口，方便其他模块根据区域编码获取城市名称。
    该函数封装了对MapDataManager实例的调用，简化了外部使用方式。
    
    Args:
        adcode: 区域编码，由数字组成的字符串
    
    Returns:
        城市名称字符串，如果未找到则返回None
    """
    # 调用全局地图数据管理器实例的区域编码转城市名称方法
    return map_data_manager.get_city_name_by_adcode(adcode)


def get_city_by_citycode(citycode: str) -> Optional[str]:
    """
    根据城市编码获取城市名称的便捷函数
    
    提供全局访问接口，方便其他模块根据城市编码获取城市名称。
    该函数封装了对MapDataManager实例的调用，简化了外部使用方式。
    
    Args:
        citycode: 城市编码，由数字组成的字符串
    
    Returns:
        城市名称字符串，如果未找到则返回None
    """
    # 调用全局地图数据管理器实例的城市编码转城市名称方法
    return map_data_manager.get_city_name_by_citycode(citycode)


if __name__ == "__main__":
    # 示例用法
    print("地图数据工具示例:")
    print("北京市的adcode:", get_adcode("北京市"))
    print("北京市的citycode:", get_citycode("北京市"))
    
    # 如果有POI数据，可以测试POI查询
    # print("POI示例:", get_poi_name("110100"))