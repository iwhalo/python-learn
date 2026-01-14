"""
高德地图API使用示例
展示了如何在项目中使用地理编码功能
"""

# 1. 地理编码功能使用示例
def geocoding_example():
    """
    地理编码使用示例 - 将地址转换为坐标
    """
    from django.conf import settings
    from invitation.views import geocode_address
    
    # 基础地理编码调用
    result = geocode_address(
        address="北京市朝阳区阜通东大街6号",
        api_key=settings.AMAP_WEB_SERVICE_KEY
    )
    
    if result:
        print(f"地理编码成功!")
        print(f"经度: {result['longitude']}")
        print(f"纬度: {result['latitude']}")
        print(f"国家: {result['country']}")
        print(f"省份: {result['province']}")
        print(f"城市: {result['city']}")
        print(f"区域: {result['district']}")
        print(f"置信度: {result['confidence']}/5")
        print(f"匹配级别: {result['level']}")
    else:
        print("地理编码失败")


# 2. 逆地理编码功能使用示例
def reverse_geocoding_example():
    """
    逆地理编码使用示例 - 将坐标转换为地址
    """
    from django.conf import settings
    from invitation.views import reverse_geocode
    
    # 逆地理编码调用
    result = reverse_geocode(
        lat=39.997213,
        lng=116.481938,
        api_key=settings.AMAP_WEB_SERVICE_KEY
    )
    
    if result:
        print(f"逆地理编码成功!")
        print(f"格式化地址: {result['formatted_address']}")
        print(f"国家: {result['country']}")
        print(f"省份: {result['province']}")
        print(f"城市: {result['city']}")
        print(f"区域: {result['district']}")
        if result['poi_list']:
            print(f"附近的POI: {result['poi_list'][0].get('name', 'N/A')}")


# 3. 带参数的高级调用示例
def advanced_usage_example():
    """
    高级使用示例 - 使用所有可用参数
    """
    from django.conf import settings
    from invitation.views import geocode_address
    
    # 使用所有参数的地理编码调用
    result = geocode_address(
        address="上海市黄浦区南京东路100号",
        api_key=settings.AMAP_WEB_SERVICE_KEY,
        city="上海",  # 指定城市范围
        output="JSON",  # 输出格式
        use_cache=True,  # 使用缓存
        daily_limit=1000  # 每日调用限制
    )
    
    if result:
        print("高级地理编码调用成功!")
        print(f"坐标: ({result['longitude']}, {result['latitude']})")
        print(f"置信度: {result['confidence']}")


# 4. 错误处理示例
def error_handling_example():
    """
    错误处理示例
    """
    from django.conf import settings
    from invitation.views import geocode_address
    
    # 尝试使用无效地址
    result = geocode_address(
        address="无效地址测试12345",
        api_key=settings.AMAP_WEB_SERVICE_KEY
    )
    
    if not result:
        print("正确处理了无效地址查询")


if __name__ == "__main__":
    print("高德地图API使用示例")
    print("="*50)
    
    # 注意：运行这些示例需要在Django环境中
    # 请在Django项目的shell中运行或使用manage.py shell
    print("请在Django环境中运行这些示例:")
    print("python manage.py shell")
    print()
    print("然后导入并调用示例函数:")
    print("from AMAP_USAGE_EXAMPLE import geocoding_example")
    print("geocoding_example()")