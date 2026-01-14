"""
城市编码表处理工具
用于处理高德地图城市编码(citycode)和区域编码(adcode)相关功能
提供城市编码与名称之间的双向转换、城市信息查询等功能
"""

import json
import os
from typing import Dict, List, Optional
from .map_data_utils import MapDataManager, get_adcode as get_adcode_from_data, get_citycode as get_citycode_from_data


class CityCodeManager:
    """
    城市编码管理器
    
    管理高德地图的城市编码(citycode)和区域编码(adcode)数据，
    提供城市编码与名称之间的查询、搜索和管理功能。
    支持从JSON文件加载和保存城市编码数据。
    """
    
    def __init__(self, data_dir: str = "config_data"):
        """
        初始化城市编码管理器
        
        设置数据目录路径，初始化内部数据结构，并加载已有的城市编码数据。
        如果指定的数据目录不存在，会自动创建该目录。
        
        Args:
            data_dir: 存放城市编码数据的目录，默认为'config_data'
        """
        # 存放城市编码数据的目录路径
        self.data_dir = data_dir
        # 城市编码表，存储城市名称到城市编码的映射
        self.city_code_table = {}
        # 区域编码映射，存储城市相关信息的完整映射表
        self.adcode_mapping = {}
        
        # 确保数据目录存在，如果不存在则创建
        os.makedirs(data_dir, exist_ok=True)
        
        # 加载城市编码数据到内存中
        self.load_city_codes()
    
    def load_city_codes(self):
        """
        加载城市编码表数据
        
        从JSON文件中加载城市编码表和区域编码映射数据到内存中。
        如果文件不存在，则相应数据结构将保持为空。
        """
        # 构建城市编码表文件的完整路径
        city_code_file = os.path.join(self.data_dir, "city_code_table.json")
        # 构建区域编码映射文件的完整路径
        mapping_file = os.path.join(self.data_dir, "city_adcode_mapping.json")
        
        # 尝试加载城市编码表，如果文件存在则读取内容
        if os.path.exists(city_code_file):
            # 以UTF-8编码打开城市编码表文件
            with open(city_code_file, 'r', encoding='utf-8') as f:
                # 解析JSON内容并存储到内部数据结构
                self.city_code_table = json.load(f)
        
        # 尝试加载区域编码映射表，如果文件存在则读取内容
        if os.path.exists(mapping_file):
            # 以UTF-8编码打开映射表文件
            with open(mapping_file, 'r', encoding='utf-8') as f:
                # 解析JSON内容并存储到内部数据结构
                self.adcode_mapping = json.load(f)
    
    def save_city_codes(self, city_codes: Dict, filename: str = "city_code_table.json"):
        """
        保存城市编码数据
        
        将城市编码数据保存到JSON格式的文件中，使用UTF-8编码，
        并设置适当的格式化选项以确保中文字符正确显示。
        
        Args:
            city_codes: 城市编码数据字典
            filename: 保存的文件名，默认为'city_code_table.json'
        """
        # 构建保存文件的完整路径
        filepath = os.path.join(self.data_dir, filename)
        # 以写入模式和UTF-8编码打开文件
        with open(filepath, 'w', encoding='utf-8') as f:
            # 将城市编码数据以JSON格式写入文件，确保ASCII字符不被转义，使用2个空格缩进
            json.dump(city_codes, f, ensure_ascii=False, indent=2)
    
    def get_citycode_by_name(self, city_name: str) -> Optional[str]:
        """
        根据城市名称获取城市编码
            
        优先从新的数据源获取城市编码，如果新数据源中没有找到，
        则回退到旧的映射表中查找。这种双重查找机制确保了数据的兼容性。
            
        Args:
            city_name: 城市名称，例如'北京市'、'上海市'等
            
        Returns:
            城市编码字符串，如果未找到对应的名称则返回None
        """
        # 优先使用新的数据源进行查询，以获得更准确和完整的结果
        result = get_citycode_from_data(city_name)
        # 检查新数据源是否返回了有效结果
        if result:
            # 如果新数据源有结果，直接返回
            return result
            
        # 如果新的数据源没有找到，回退到旧的映射表逻辑
        if not self.adcode_mapping:
            # 如果映射表为空，直接返回None
            return None
                
        # 遍历映射表中的所有城市信息
        for city_info in self.adcode_mapping.get("districts", []):
            # 检查当前城市信息的名称是否与查询名称匹配
            if city_info.get("name") == city_name:
                # 如果匹配，返回对应的城市编码
                return city_info.get("citycode")
                    
        # 如果遍历完所有城市信息仍未找到匹配项，返回None
        return None
    
    def get_adcode_by_name(self, city_name: str) -> Optional[str]:
        """
        根据城市名称获取区域编码
            
        优先从新的数据源获取区域编码，如果新数据源中没有找到，
        则回退到旧的映射表中查找。这种双重查找机制确保了数据的兼容性。
            
        Args:
            city_name: 城市名称，例如'北京市'、'上海市'等
            
        Returns:
            区域编码字符串，如果未找到对应的名称则返回None
        """
        # 优先使用新的数据源进行查询，以获得更准确和完整的结果
        result = get_adcode_from_data(city_name)
        # 检查新数据源是否返回了有效结果
        if result:
            # 如果新数据源有结果，直接返回
            return result
            
        # 如果新的数据源没有找到，回退到旧的映射表逻辑
        if not self.adcode_mapping:
            # 如果映射表为空，直接返回None
            return None
                
        # 遍历映射表中的所有城市信息
        for city_info in self.adcode_mapping.get("districts", []):
            # 检查当前城市信息的名称是否与查询名称匹配
            if city_info.get("name") == city_name:
                # 如果匹配，返回对应的区域编码
                return city_info.get("adcode")
                    
        # 如果遍历完所有城市信息仍未找到匹配项，返回None
        return None
    
    def get_city_info_by_adcode(self, adcode: str) -> Optional[Dict]:
        """
        根据区域编码获取城市信息
            
        通过指定的区域编码查找完整的城市信息，包括城市名称、
        城市编码和其他相关信息。
            
        Args:
            adcode: 区域编码，用于查询对应的城市信息
            
        Returns:
            城市信息字典，包含城市名称、编码等信息，如果未找到返回None
        """
        # 检查映射表是否为空
        if not self.adcode_mapping:
            # 如果映射表为空，直接返回None
            return None
                
        # 遍历映射表中的所有城市信息
        for city_info in self.adcode_mapping.get("districts", []):
            # 检查当前城市信息的区域编码是否与查询编码匹配
            if city_info.get("adcode") == adcode:
                # 如果匹配，返回完整的城市信息字典
                return city_info
                    
        # 如果遍历完所有城市信息仍未找到匹配项，返回None
        return None
    
    def search_cities_by_keyword(self, keyword: str) -> List[Dict]:
        """
        根据关键词搜索城市
            
        在城市名称和城市编码中进行模糊匹配，返回包含关键词的城市信息。
        支持对城市名称和城市编码的精确匹配搜索。
            
        Args:
            keyword: 搜索关键词，可以是城市名称的一部分或编码的一部分
            
        Returns:
            匹配的城市信息列表，每个元素包含城市名称、编码等信息
        """
        # 检查映射表是否为空
        if not self.adcode_mapping:
            # 如果映射表为空，返回空列表
            return []
                
        # 初始化结果列表，用于存储匹配的城市信息
        results = []
        # 遍历映射表中的所有城市信息
        for city_info in self.adcode_mapping.get("districts", []):
            # 检查关键词是否存在于城市名称或城市编码中
            if keyword in city_info.get("name", "") or keyword in city_info.get("citycode", ""):
                # 如果匹配，将城市信息添加到结果列表
                results.append(city_info)
                    
        # 返回匹配的城市信息列表
        return results


# 创建全局城市编码管理器实例，用于在整个应用中共享城市编码数据
city_code_manager = CityCodeManager()


def get_city_code(city_name: str) -> Optional[str]:
    """
    获取城市编码的便捷函数
    
    提供全局访问接口，方便其他模块根据城市名称获取城市编码。
    该函数封装了对CityCodeManager实例的调用，简化了外部使用方式。
    
    Args:
        city_name: 城市名称，例如'北京市'、'上海市'等
    
    Returns:
        城市编码字符串，如果未找到则返回None
    """
    # 调用全局城市编码管理器实例的城市编码查询方法
    return city_code_manager.get_citycode_by_name(city_name)


def get_adcode(city_name: str) -> Optional[str]:
    """
    获取区域编码的便捷函数
    
    提供全局访问接口，方便其他模块根据城市名称获取区域编码。
    该函数封装了对CityCodeManager实例的调用，简化了外部使用方式。
    
    Args:
        city_name: 城市名称，例如'北京市'、'上海市'等
    
    Returns:
        区域编码字符串，如果未找到则返回None
    """
    # 调用全局城市编码管理器实例的区域编码查询方法
    return city_code_manager.get_adcode_by_name(city_name)


if __name__ == "__main__":
    # 示例用法
    print("城市编码工具示例:")
    print("北京市的citycode:", get_city_code("北京市"))
    print("北京市的adcode:", get_adcode("北京市"))