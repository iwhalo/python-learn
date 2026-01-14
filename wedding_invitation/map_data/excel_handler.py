"""
Excel数据处理器
用于处理高德地图的Excel格式数据文件
提供对POI分类数据和城市编码数据的读取、解析和导出功能
"""

import os
import pandas as pd
from typing import Dict, List, Optional
from .models import POICategory, CityInfo, DistrictInfo


class ExcelDataHandler:
    """
    Excel数据处理器
    
    专门用于处理高德地图的Excel格式数据文件，包括POI分类数据和城市编码数据。
    提供数据的读取、解析、转换和导出功能，支持将Excel数据转换为内部数据模型。
    """
    
    def __init__(self, data_dir: str = "map_files"):
        """
        初始化Excel数据处理器
        
        设置数据目录路径，用于定位POI和城市编码的Excel文件。
        该处理器依赖pandas库来读取和解析Excel文件内容。
        
        Args:
            data_dir: 存放Excel数据文件的目录，默认为'map_files'
        """
        # 存储Excel数据文件的目录路径
        self.data_dir = data_dir
    
    def load_poi_data(self, filename: str = "高德POI分类与编码（中英文）_V1.06_20230208.xlsx") -> List[POICategory]:
        """
        加载POI分类数据
            
        从指定的Excel文件中读取POI分类信息，包括POI编码、中文名称、英文名称等。
        解析后的数据转换为POICategory对象列表，供系统内部使用。
            
        Args:
            filename: POI数据Excel文件名，默认为高德地图POI分类标准文件
            
        Returns:
            POI分类对象列表，如果加载失败则返回空列表
        """
        # 构建POI数据文件的完整路径，Amap_poicode子目录存放POI分类数据
        poi_dir = os.path.join(self.data_dir, "Amap_poicode")
        # 完整的POI Excel文件路径
        poi_xlsx = os.path.join(poi_dir, filename)
            
        # 检查POI数据文件是否存在
        if not os.path.exists(poi_xlsx):
            # 如果文件不存在，抛出文件未找到异常
            raise FileNotFoundError(f"POI数据文件不存在: {poi_xlsx}")
            
        try:
            # 使用pandas读取Excel文件内容到DataFrame
            df = pd.read_excel(poi_xlsx)
            # 初始化POI分类对象列表
            poi_categories = []
                
            # 遍历DataFrame中的每一行数据，将其转换为POICategory对象
            for _, row in df.iterrows():
                # 创建POICategory对象，提取必要的字段
                poi = POICategory(
                    # POI编码，转换为字符串类型
                    code=str(row.get('code', '')),
                    # POI中文名称
                    name=row.get('name', ''),
                    # POI英文名称，如果不存在则为None
                    english_name=row.get('english_name', None),
                    # 父级POI编码，用于构建POI分类层级关系
                    parent_code=row.get('parent_code', None)
                )
                # 将创建的POI对象添加到列表中
                poi_categories.append(poi)
                    
            # 返回解析完成的POI分类对象列表
            return poi_categories
                
        except Exception as e:
            # 如果加载过程中发生异常，打印错误信息并返回空列表
            print(f"加载POI数据失败: {e}")
            return []
    
    def load_city_data(self, filename: str = "AMap_adcode_citycode.xlsx") -> List[CityInfo]:
        """
        加载城市编码数据
            
        从指定的Excel文件中读取城市编码信息，包括区域编码(adcode)、城市编码(citycode)、
        城市中心坐标等。解析后的数据转换为CityInfo对象列表，支持多种城市名称列名格式。
            
        Args:
            filename: 城市编码数据Excel文件名，默认为高德地图城市编码标准文件
            
        Returns:
            城市信息对象列表，如果加载失败则返回空列表
        """
        # 构建城市数据文件的完整路径，AMap_adcode_citycode子目录存放城市编码数据
        city_dir = os.path.join(self.data_dir, "AMap_adcode_citycode")
        # 完整的城市编码Excel文件路径
        city_xlsx = os.path.join(city_dir, filename)
            
        # 检查城市数据文件是否存在
        if not os.path.exists(city_xlsx):
            # 如果文件不存在，抛出文件未找到异常
            raise FileNotFoundError(f"城市数据文件不存在: {city_xlsx}")
            
        try:
            # 使用pandas读取Excel文件内容到DataFrame
            df = pd.read_excel(city_xlsx)
            # 初始化城市信息对象列表
            cities = []
                
            # 检查DataFrame中有哪些列，并尝试找到代表城市名称的列
            columns = df.columns.tolist()
            city_name_col = None
                
            # 尝试几种可能的城市名称列名，以支持不同格式的Excel文件
            possible_city_name_cols = ['city_name', 'name', 'cityname', 'city', '地区名称', '城市名称', '城市']
            for col in possible_city_name_cols:
                if col in columns:
                    city_name_col = col
                    break
                
            if city_name_col is None:
                # 如果没找到标准城市名称列，尝试使用第一列作为城市名称
                city_name_col = columns[0] if columns else 'name'
                
            # 检查adcode列是否存在，这是必需的关键列
            if 'adcode' not in columns:
                raise KeyError("Excel文件中缺少'adcode'列")
                
            # 按照adcode和城市名称分组处理城市数据，处理同一城市的多个区域信息
            grouped = df.groupby(['adcode', city_name_col])
                
            for (adcode, city_name), group in grouped:
                # 获取该城市的第一行数据作为城市基本信息
                first_row = group.iloc[0]
                    
                # 创建CityInfo对象，包含城市的基本信息
                city = CityInfo(
                    # 城市名称
                    name=city_name,
                    # 区域编码
                    adcode=str(adcode),
                    # 城市编码
                    citycode=str(first_row.get('citycode', '')),
                    # 城市中心坐标
                    center=first_row.get('center', ''),
                    # 城市等级（如：city, district等）
                    level=first_row.get('level', 'city')
                )
                    
                # 遍历分组中的每一行数据，添加区域信息到城市对象
                for _, row in group.iterrows():
                    # 创建区域信息对象
                    district = DistrictInfo(
                        # 区域名称
                        name=row.get('district_name', ''),
                        # 区域编码
                        adcode=str(row.get('district_adcode', '')),
                        # 区域对应的城市编码
                        citycode=str(row.get('citycode', '')),
                        # 区域中心坐标
                        center=row.get('center', ''),
                        # 区域等级
                        level=row.get('level', 'district')
                    )
                    # 将区域信息添加到城市对象的区域列表中
                    city.districts.append(district)
                    
                # 将创建的城市信息对象添加到城市列表
                cities.append(city)
                    
            # 返回解析完成的城市信息对象列表
            return cities
                
        except Exception as e:
            # 如果加载过程中发生异常，打印错误信息并返回空列表
            print(f"加载城市数据失败: {e}")
            return []
    
    def export_poi_data(self, poi_categories: List[POICategory], output_path: str):
        """
        导出POI数据到Excel文件
        
        将POICategory对象列表转换为Excel格式文件，包含POI编码、名称、
        英文名称和父级编码等信息。导出的文件可用于数据备份或与其他系统交换数据。
        
        Args:
            poi_categories: POI分类对象列表，包含待导出的POI数据
            output_path: 输出文件路径，指定导出的Excel文件保存位置
        """
        # 初始化数据列表，用于存储准备导出的POI数据
        data = []
        # 遍历POI分类对象列表，将每个对象转换为字典格式
        for poi in poi_categories:
            # 将POI对象的属性转换为字典并添加到数据列表
            data.append({
                # POI编码
                'code': poi.code,
                # POI中文名称
                'name': poi.name,
                # POI英文名称
                'english_name': poi.english_name,
                # 父级POI编码
                'parent_code': poi.parent_code
            })
        
        # 将数据列表转换为pandas DataFrame
        df = pd.DataFrame(data)
        # 将DataFrame保存为Excel文件，不包含行索引
        df.to_excel(output_path, index=False)
    
    def export_city_data(self, cities: List[CityInfo], output_path: str):
        """
        导出城市数据到Excel文件
        
        将CityInfo对象列表转换为Excel格式文件，包含城市基本信息和区域信息。
        数据以平面表格形式存储，每个城市及其下辖区域分别占用一行。
        
        Args:
            cities: 城市信息对象列表，包含待导出的城市和区域数据
            output_path: 输出文件路径，指定导出的Excel文件保存位置
        """
        # 初始化数据列表，用于存储准备导出的城市和区域数据
        data = []
        # 遍历城市信息对象列表
        for city in cities:
            # 添加城市级别的信息，区域相关字段留空
            data.append({
                # 城市名称
                'city_name': city.name,
                # 城市区域编码
                'adcode': city.adcode,
                # 城市编码
                'citycode': city.citycode,
                # 城市中心坐标
                'center': city.center,
                # 级别（city或district）
                'level': city.level,
                # 区域名称，城市级别此项为空
                'district_name': '',  # 城市级别没有具体的区名
                # 区域编码，城市级别此项为空
                'district_adcode': ''
            })
            
            # 遍历城市下辖的每个区域，添加区域级别的信息
            for district in city.districts:
                # 添加区域级别的信息
                data.append({
                    # 所属城市名称
                    'city_name': city.name,
                    # 所属城市区域编码
                    'adcode': city.adcode,
                    # 所属城市编码
                    'citycode': city.citycode,
                    # 区域中心坐标
                    'center': district.center,
                    # 级别（district）
                    'level': district.level,
                    # 区域名称
                    'district_name': district.name,
                    # 区域编码
                    'district_adcode': district.adcode
                })
        
        # 将数据列表转换为pandas DataFrame
        df = pd.DataFrame(data)
        # 将DataFrame保存为Excel文件，不包含行索引
        df.to_excel(output_path, index=False)


# 全局数据处理器实例
excel_handler = ExcelDataHandler()