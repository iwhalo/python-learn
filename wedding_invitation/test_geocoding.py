"""
测试地理编码功能的脚本
"""

import os
import sys
import django
from django.conf import settings

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_invitation.settings')
django.setup()

from invitation.views import geocode_address, reverse_geocode
from django.conf import settings

def test_geocoding():
    """测试地理编码功能"""
    print("开始测试地理编码功能...")
    
    # 测试地址
    test_addresses = [
        "北京市朝阳区阜通东大街6号",
        "上海市黄浦区南京东路100号",
        "广州市天河区天河路208号",
        "深圳市南山区科技园南区科技南路18号",
    ]
    
    for address in test_addresses:
        print(f"\n测试地址: {address}")
        # 测试带城市参数的地理编码
        city_name = None
        if '市' in address[:15]:
            import re
            city_match = re.search(r'(?:北京市|天津市|上海市|重庆市|[一-龥]{1,3}市)', address[:30])
            if city_match:
                city_name = city_match.group()
                if city_name.endswith('市'):
                    city_name = city_name[:-1]
        
        result_with_city = geocode_address(address, settings.AMAP_API_KEY, city=city_name)
        if result_with_city:
            print(f"  ✓ 带城市参数地理编码成功:")
            print(f"    经度: {result_with_city['longitude']}")
            print(f"    纬度: {result_with_city['latitude']}")
            print(f"    国家: {result_with_city['country']}")
            print(f"    省份: {result_with_city['province']}")
            print(f"    城市: {result_with_city['city']}")  
            print(f"    区域: {result_with_city['district']}")
            print(f"    匹配级别: {result_with_city['level']}")
            print(f"    置信度: {result_with_city['confidence']}/5")
            print(f"    商圈: {result_with_city['business_area']}")
        else:
            print(f"  ✗ 带城市参数地理编码失败")
        
        # 测试不带城市参数的地理编码
        result_without_city = geocode_address(address, settings.AMAP_API_KEY)
        if result_without_city:
            print(f"  ✓ 不带城市参数地理编码成功:")
            print(f"    经度: {result_without_city['longitude']}")
            print(f"    纬度: {result_without_city['latitude']}")
            print(f"    匹配级别: {result_without_city['level']}")
            print(f"    置信度: {result_without_city['confidence']}/5")
        else:
            print(f"  ✗ 不带城市参数地理编码失败")
    
    # 测试不同输出格式
    print("\n" + "-"*50)
    print("测试不同输出格式...")
    test_addr = "北京市海淀区中关村大街49号"
    result_json = geocode_address(test_addr, settings.AMAP_API_KEY, output='JSON')
    if result_json:
        print(f"JSON格式编码成功: {result_json['longitude']}, {result_json['latitude']}")
    
    # 测试逆地理编码
    print("\n" + "="*50)
    print("开始测试逆地理编码功能...")
    
    test_coordinates = [
        (39.997213, 116.481938),  # 北京某地
        (31.239688, 121.478941),  # 上海某地
    ]
    
    for lat, lng in test_coordinates:
        print(f"\n测试坐标: ({lng}, {lat})")
        result = reverse_geocode(lat, lng, settings.AMAP_API_KEY)
        
        if result:
            print(f"  ✓ 逆地理编码成功:")
            print(f"    格式化地址: {result['formatted_address']}")
            print(f"    国家: {result['country']}")
            print(f"    省份: {result['province']}")
            print(f"    城市: {result['city']}")
            print(f"    区域: {result['district']}")
            print(f"    乡镇: {result['township']}")
            if result['poi_list']:
                print(f"    POI数量: {len(result['poi_list'])}")
                if len(result['poi_list']) > 0:
                    print(f"    第一个POI: {result['poi_list'][0].get('name', 'N/A')}")
        else:
            print(f"  ✗ 逆地理编码失败")

if __name__ == "__main__":
    test_geocoding()