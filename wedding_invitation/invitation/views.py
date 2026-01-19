"""
婚礼邀请函应用的视图模块

这个模块包含了婚礼邀请函网站的所有视图函数，
处理HTTP请求并返回相应的响应，包括页面渲染、
数据处理和API接口等功能。
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import logging
from .models import WeddingEvent, Guest, GalleryImage, PageVisit, GeocodingCache, APIUsageStats
from map_data.poi_utils import get_poi_name, search_poi
from map_data.city_code_utils import get_adcode, get_city_code
import json
import os
import urllib.parse
import urllib.request

# 配置日志记录器，用于记录应用运行状态和错误信息
logger = logging.getLogger('invitation')

# 定义常量 - API调用频率限制
DEFAULT_DAILY_LIMIT = 1000
# 定义常量 - 地图默认缩放级别
DEFAULT_MAP_ZOOM = 15
# 定义常量 - 默认中心坐标(北京天安门)
DEFAULT_CENTER_LAT = 39.90923
DEFAULT_CENTER_LNG = 116.397428


# 高德地图地理编码函数，将地址转换为经纬度坐标
# 用于婚礼地址的地理位置定位，以便在地图上准确显示婚礼地点
# 包含完整的错误处理和API调用限制管理
# 参数: address - 需要地理编码的地址字符串
# 参数: api_key - 高德地图API密钥，用于身份验证
# 参数: city - 可选的城市名称，用于限制搜索范围
# 参数: sig - 可选的数字签名，用于安全验证
# 参数: output - 返回数据格式，支持JSON或XML
# 参数: callback - 可选的回调函数名，用于JSONP请求
# 参数: use_cache - 是否使用缓存，默认为True以提高性能
# 参数: daily_limit - 每日API调用限制，默认使用常量值
# 返回值: 包含地理编码信息的字典，失败时返回None
def geocode_address(address, api_key, city=None, sig=None, output='JSON', callback=None, use_cache=True,
                    daily_limit=DEFAULT_DAILY_LIMIT):
    """
    使用高德地图API将地址转换为经纬度坐标
    
    这个函数负责将婚礼地址转换为地图坐标，用于在地图上显示婚礼地点。
    包含完整的错误处理和API密钥验证。
    
    Args:
        address (str): 需要地理编码的地址
        api_key (str): 高德地图API密钥
        city (str, optional): 指定查询的城市，可选参数
        sig (str, optional): 数字签名，可选参数
        output (str, optional): 返回数据格式，JSON或XML，默认JSON
        callback (str, optional): 回调函数名，仅在output为JSON时有效
        use_cache (bool, optional): 是否使用缓存，默认True
        daily_limit (int, optional): 每日调用限制，默认1000次
    
    Returns:
        dict or None: 包含地理编码信息的字典，失败时返回None
    """
    # 记录函数调用开始，包含地址信息和API密钥长度用于安全审计
    logger.info(f"地理编码函数被调用 - 地址: {address}, API密钥长度: {len(api_key) if api_key else 0}")
    # 详细记录API密钥验证过程
    logger.debug(f"开始验证API密钥 - 地址: {address}")
    # 验证API密钥是否存在且不是默认值
    if not api_key or api_key == 'YOUR_AMAP_API_KEY_HERE':
        # 记录API密钥验证失败的情况
        logger.warning("高德地图API密钥未配置或使用默认值")
        # 更新API调用统计，标记为失败
        APIUsageStats.increment_call('geocode', success=False)
        # 返回None表示地理编码失败
        return None
        # 详细记录API密钥验证结果
        logger.debug(f"API密钥验证结果 - 有效: {bool(api_key and api_key != 'YOUR_AMAP_API_KEY_HERE')}")

    # 检查API调用是否达到每日限制，防止超出配额
    logger.debug(f"检查地理编码API调用限制 - 当前限制: {daily_limit}, 地址: {address}")
    if not APIUsageStats.check_rate_limit('geocode', daily_limit):
        # 记录达到调用限制的情况
        logger.warning(f"地理编码API已达到每日调用限制 ({daily_limit}次) - 地址: {address}")
        # 返回None表示无法继续处理
        return None
        # 详细记录限制检查结果
        logger.debug(f"API调用限制检查结果 - 未达限制: {APIUsageStats.check_rate_limit('geocode', daily_limit)}")

    # 首先检查缓存，提高性能并减少API调用
    logger.debug(f"检查地理编码缓存 - 地址: {address}, 使用缓存: {use_cache}")
    if use_cache:
        # 从缓存中获取结果
        cached_result = GeocodingCache.get_cached_result(address)
        if cached_result:
            # 记录缓存命中的情况
            logger.info(f"地理编码命中缓存 - 地址: {address}")
            # 返回缓存的结果
            return cached_result
            # 详细记录缓存检查结果
            logger.debug(f"缓存检查结果 - 命中: {bool(cached_result)}")
        else:
            # 记录缓存未命中的情况
            logger.debug(f"地理编码未命中缓存 - 地址: {address}")
    else:
        # 记录未使用缓存的情况
        logger.debug(f"跳过缓存检查 - 地址: {address}")

    # 记录开始地理编码的过程
    logger.info(f"开始地理编码 - 地址: {address}, 城市: {city}")

    # 构造请求URL和参数，用于高德地图地理编码API
    logger.debug(f"构造地理编码请求参数 - 地址: {address}, 输出格式: {output}")
    base_url = "https://restapi.amap.com/v3/geocode/geo"
    # 初始化请求参数字典
    params = {
        'key': api_key,  # API密钥
        'address': address,  # 需要编码的地址
        'output': output  # 输出格式
    }
    # 详细记录参数构建结果
    logger.debug(f"请求参数构建完成 - 参数数量: {len(params)}")

    # 添加可选参数
    if city:
        params['city'] = city
    if sig:
        params['sig'] = sig
    if callback and output.lower() == 'json':
        params['callback'] = callback

    try:
        # 编码URL参数
        logger.debug(f"编码地理编码请求参数 - 地址: {address}, 城市: {city}")
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{encoded_params}"

        logger.debug(f"发送地理编码请求 - URL: {full_url[:100]}...")

        # 通过urllib发送HTTP GET请求到高德地图API
        logger.debug(f"准备发送HTTP请求 - URL长度: {len(full_url)}")
        with urllib.request.urlopen(full_url) as response:
            # 读取响应数据并解码为UTF-8格式
            response_data = response.read().decode('utf-8')
            # 记录响应数据长度
            logger.debug(f"收到响应数据 - 长度: {len(response_data)} 字符")

            # 如果使用JSONP格式，需要移除回调函数包装
            logger.debug(f"处理JSONP回调 - 有回调: {bool(callback)}, 输出格式: {output}")
            if callback and output.lower() == 'json':
                # 移除JSONP格式的回调包装以提取纯JSON数据
                if response_data.startswith(callback):
                    # 查找回调函数参数的起始和结束位置
                    start_idx = response_data.find('(') + 1
                    end_idx = response_data.rfind(')')
                    # 验证找到的位置是否有效
                    if start_idx > 0 and end_idx > start_idx:
                        # 提取回调函数参数中的JSON数据
                        response_data = response_data[start_idx:end_idx]
                        logger.debug(f"JSONP包装移除成功 - 提取数据长度: {len(response_data)}")
                else:
                    logger.debug(f"响应数据不以回调函数开头 - 回调: {callback}")
            else:
                logger.debug(f"非JSONP格式，跳过包装处理 - 回调: {bool(callback)}, 输出: {output}")

            # 将响应数据解析为JSON对象
            logger.debug(f"开始解析JSON响应 - 数据长度: {len(response_data)}")
            data = json.loads(response_data)
            logger.debug(f"JSON解析完成 - 响应状态: {data.get('status', 'unknown')}")

        # 记录API响应的详细信息
        logger.debug(
            f"地理编码响应 - 状态: {data.get('status')}, 结果数: {len(data.get('geocodes', []))}, 信息: {data.get('info', 'unknown')}")

        # 详细检查API返回的各种错误状态
        logger.debug(f"检查API响应状态 - 信息代码: {data.get('info', 'unknown')}")
        if data.get('info') == 'INVALID_USER_KEY':
            # API密钥无效错误处理
            logger.error(f"高德地图API密钥无效 - 请检查您的API密钥配置")
            # 更新API调用统计，标记为失败
            APIUsageStats.increment_call('geocode', success=False)
            # 返回None表示地理编码失败
            return None
        elif data.get('info') == 'USER_KEY_RECYCLED':
            # API密钥被回收错误处理
            logger.error(f"高德地图API密钥已被回收 - 请重新申请API密钥")
            # 更新API调用统计，标记为失败
            APIUsageStats.increment_call('geocode', success=False)
            # 返回None表示地理编码失败
            return None
        elif data.get('info') == 'OVER_LIMIT':
            # API调用次数超限错误处理
            logger.warning(f"高德地图API调用次数超限 - 地址: {address}")
            # 更新API调用统计，标记为失败
            APIUsageStats.increment_call('geocode', success=False)
            # 返回None表示地理编码失败
            return None
        elif data.get('info') == 'USERKEY_PLAT_NOMATCH':
            # API密钥与平台类型不匹配错误处理
            logger.error(
                f"高德地图API密钥与平台类型不匹配 - 请检查您申请的API密钥类型是否适用于Web服务 - 地址: {address}")
            # 更新API调用统计，标记为失败
            APIUsageStats.increment_call('geocode', success=False)
            # 返回None表示地理编码失败
            return None
        else:
            # 记录未预期的API响应信息
            logger.debug(f"API响应信息代码 - 代码: {data.get('info', 'unknown')}")

        # 解析成功的地理编码响应结果
        logger.debug(f"解析地理编码结果 - 状态: {data.get('status')}, 地理编码数量: {len(data.get('geocodes', []))}")
        if data.get('status') == '1' and data.get('geocodes'):
            # 获取第一个地理编码结果
            geocode_info = data['geocodes'][0]
            # 从位置字符串中提取经纬度
            location = geocode_info['location']
            lng, lat = location.split(',')
            # 记录提取的经纬度信息
            logger.debug(f"提取经纬度 - 经度: {lng}, 纬度: {lat}")

            # 构建完整的地理编码信息字典，包含所有相关字段
            logger.debug("开始构建地理编码结果字典")
            result = {
                'longitude': float(lng),  # 经度，转换为浮点数
                'latitude': float(lat),  # 纬度，转换为浮点数
                'formatted_address': geocode_info.get('formatted_address', ''),  # 格式化的完整地址
                'country': geocode_info.get('country', ''),  # 国家
                'province': geocode_info.get('province', ''),  # 省份
                'city': geocode_info.get('city', ''),  # 城市
                'district': geocode_info.get('district', ''),  # 区县
                'street': geocode_info.get('street', ''),  # 街道
                'number': geocode_info.get('number', ''),  # 门牌号
                'adcode': geocode_info.get('adcode', ''),  # 区域码
                'level': geocode_info.get('level', ''),  # 匹配级别
                'confidence': calculate_confidence(geocode_info.get('level', '')),  # 计算置信度
                'business_area': geocode_info.get('business_area', []),  # 商圈信息
                'neighborhood': geocode_info.get('neighborhood', {})  # 社区信息
            }
            # 记录结果构建完成
            logger.debug(f"地理编码结果构建完成 - 字段数量: {len(result)}")

            # 记录地理编码成功的详细信息
            logger.info(
                f"地理编码成功 - 地址: {address}, 坐标: ({lng}, {lat}), 匹配级别: {geocode_info.get('level', '')}, 置信度: {calculate_confidence(geocode_info.get('level', ''))}")

            # 根据配置决定是否将结果存入缓存以提高后续查询性能
            logger.debug(f"处理地理编码结果缓存 - 使用缓存: {use_cache}")
            if use_cache:
                # 将地理编码结果存入缓存
                GeocodingCache.set_cache_result(address, result)
                logger.debug(f"地理编码结果已存入缓存 - 地址: {address}")
            else:
                logger.debug(f"跳过地理编码结果存入缓存 - 地址: {address}")

            # 更新API调用统计，标记为成功
            logger.debug(f"更新API调用统计 - 类型: geocode, 成功: True")
            APIUsageStats.increment_call('geocode', success=True)
            # 返回成功解析的地理编码结果
            logger.debug(f"返回地理编码结果 - 字段数: {len(result)}")
            return result
        else:
            error_info = data.get('info', 'Unknown error')
            logger.warning(f"地理编码失败 - 地址: {address}, 错误: {error_info}")
            APIUsageStats.increment_call('geocode', success=False)
            return None

    # 捕获HTTP错误，通常是服务器返回错误状态码
    except urllib.error.HTTPError as e:
        # 记录HTTP错误的详细信息
        logger.error(f"地理编码HTTP错误 - 地址: {address}, 错误代码: {e.code}, 原因: {e.reason}")
        # 更新API调用统计，标记为失败
        APIUsageStats.increment_call('geocode', success=False)
        # 返回None表示地理编码失败
        return None
    # 捕获URL错误，通常是网络连接问题
    except urllib.error.URLError as e:
        # 记录URL错误的详细信息
        logger.error(f"地理编码URL错误 - 地址: {address}, 错误: {str(e)}")
        # 更新API调用统计，标记为失败
        APIUsageStats.increment_call('geocode', success=False)
        # 返回None表示地理编码失败
        return None
    # 捕获JSON解析错误，通常是API返回非JSON格式数据
    except json.JSONDecodeError as e:
        # 记录JSON解析错误的详细信息
        logger.error(f"地理编码响应JSON解析失败 - 地址: {address}, 错误: {str(e)}")
        # 更新API调用统计，标记为失败
        APIUsageStats.increment_call('geocode', success=False)
        # 返回None表示地理编码失败
        return None
    # 捕获所有其他未预期的异常
    except Exception as e:
        # 记录通用错误的详细信息，包含堆栈跟踪
        logger.error(f"地理编码请求失败 - 地址: {address}, 错误: {str(e)}", exc_info=True)
        # 更新API调用统计，标记为失败
        APIUsageStats.increment_call('geocode', success=False)
        # 返回None表示地理编码失败
        return None
    # 记录异常处理完成
    finally:
        logger.debug(f"地理编码请求处理完成 - 地址: {address}")


def calculate_confidence(level):
    """
    根据匹配级别计算置信度分数
    
    Args:
        level (str): 匹配级别
        
    Returns:
        int: 置信度分数 (1-5)
    """
    confidence_mapping = {
        '地级市': 2,
        '区县': 3,
        '乡镇': 3,
        '交叉口': 4,
        '门牌号': 5,
        '兴趣点': 5,
        '道路': 4
    }
    return confidence_mapping.get(level, 3)  # 默认为3


# 高德地图逆地理编码函数，将经纬度坐标转换为详细地址
# 用于将坐标点转换为可读的地址信息
# 包含完整的错误处理和API调用限制管理
# 参数: lat - 纬度坐标
# 参数: lng - 经度坐标
# 参数: api_key - 高德地图API密钥，用于身份验证
# 参数: extensions - 返回数据扩展级别，'all'或'base'
# 参数: use_cache - 是否使用缓存，默认为True以提高性能
# 参数: daily_limit - 每日API调用限制，默认使用常量值
# 返回值: 包含地址信息的字典，失败时返回None
def reverse_geocode(lat, lng, api_key, extensions='all', use_cache=True, daily_limit=DEFAULT_DAILY_LIMIT):
    """
    使用高德地图API进行逆地理编码（坐标转地址）
    
    Args:
        lat (float): 纬度
        lng (float): 经度
        api_key (str): 高德地图API密钥
        extensions (str, optional): 返回结果控制，'all'或'base'
        use_cache (bool, optional): 是否使用缓存，默认True
        daily_limit (int, optional): 每日调用限制，默认1000次
    
    Returns:
        dict or None: 包含地址信息的字典，失败时返回None
    """
    logger.info(f"逆地理编码函数被调用 - 坐标: ({lng}, {lat}), API密钥长度: {len(api_key) if api_key else 0}")
    if not api_key or api_key == 'YOUR_AMAP_API_KEY_HERE':
        logger.warning("高德地图API密钥未配置或使用默认值")
        APIUsageStats.increment_call('reverse_geocode', success=False)
        return None

    # 检查是否达到每日调用限制
    if not APIUsageStats.check_rate_limit('reverse_geocode', daily_limit):
        logger.warning(f"逆地理编码API已达到每日调用限制 ({daily_limit}次) - 坐标: ({lng}, {lat})")
        return None

    # 创建缓存键
    cache_key = f"reverse_{lng}_{lat}_{extensions}"

    # 首先检查缓存
    if use_cache:
        cached_result = GeocodingCache.get_cached_result(cache_key)
        if cached_result:
            logger.info(f"逆地理编码命中缓存 - 坐标: ({lng}, {lat})")
            return cached_result

    logger.info(f"开始逆地理编码 - 坐标: ({lng}, {lat})")

    # 构造请求URL和参数
    base_url = "https://restapi.amap.com/v3/geocode/regeo"
    params = {
        'key': api_key,
        'location': f"{lng},{lat}",
        'extensions': extensions
    }

    try:
        # 编码URL参数
        logger.debug(f"编码逆地理编码请求参数 - 坐标: ({lng}, {lat})")
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{encoded_params}"

        logger.debug(f"发送逆地理编码请求 - URL: {full_url[:100]}...")

        # 发送HTTP请求
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))

        logger.debug(f"逆地理编码响应 - 状态: {data.get('status')}, 信息: {data.get('info')}")

        # 检查API密钥状态和各种错误情况
        if data.get('info') == 'INVALID_USER_KEY':
            logger.error("高德地图API密钥无效 - 请检查您的API密钥配置")
            APIUsageStats.increment_call('reverse_geocode', success=False)
            return None
        elif data.get('info') == 'USER_KEY_RECYCLED':
            logger.error("高德地图API密钥已被回收 - 请重新申请API密钥")
            APIUsageStats.increment_call('reverse_geocode', success=False)
            return None
        elif data.get('info') == 'OVER_LIMIT':
            logger.warning(f"高德地图API调用次数超限 - 坐标: ({lng}, {lat})")
            APIUsageStats.increment_call('reverse_geocode', success=False)
            return None
        elif data.get('info') == 'USERKEY_PLAT_NOMATCH':
            logger.error(
                f"高德地图API密钥与平台类型不匹配 - 请检查您申请的API密钥类型是否适用于Web服务 - 坐标: ({lng}, {lat})")
            APIUsageStats.increment_call('reverse_geocode', success=False)
            return None

        # 解析逆地理编码结果
        if data.get('status') == '1' and data.get('regeocode'):
            regeo_info = data['regeocode']
            address_component = regeo_info.get('addressComponent', {})

            # 构建完整的逆地理编码信息
            result = {
                'formatted_address': regeo_info.get('formatted_address', ''),
                'country': address_component.get('country', ''),
                'province': address_component.get('province', ''),
                'city': address_component.get('city', ''),
                'district': address_component.get('district', ''),
                'township': address_component.get('township', ''),
                'neighborhood': address_component.get('neighborhood', {}).get('name', ''),
                'building': address_component.get('building', {}).get('name', ''),
                'street_number': address_component.get('streetNumber', {}).get('number', ''),
                'street': address_component.get('streetNumber', {}).get('street', ''),
                'poi_list': regeo_info.get('pois', []),
                'road_list': regeo_info.get('roads', [])
            }

            logger.info(f"逆地理编码成功 - 坐标: ({lng}, {lat}), 地址: {result['formatted_address']}")

            # 将结果存入缓存
            if use_cache:
                GeocodingCache.set_cache_result(cache_key, result)

            APIUsageStats.increment_call('reverse_geocode', success=True)
            return result
        else:
            error_info = data.get('info', 'Unknown error')
            logger.warning(f"逆地理编码失败 - 坐标: ({lng}, {lat}), 错误: {error_info}")
            APIUsageStats.increment_call('reverse_geocode', success=False)
            return None

    except urllib.error.HTTPError as e:
        logger.error(f"逆地理编码HTTP错误 - 坐标: ({lng}, {lat}), 错误代码: {e.code}, 原因: {e.reason}")
        APIUsageStats.increment_call('reverse_geocode', success=False)
        return None
    except urllib.error.URLError as e:
        logger.error(f"逆地理编码URL错误 - 坐标: ({lng}, {lat}), 错误: {str(e)}")
        APIUsageStats.increment_call('reverse_geocode', success=False)
        return None
    except json.JSONDecodeError as e:
        logger.error(f"逆地理编码响应JSON解析失败 - 坐标: ({lng}, {lat}), 错误: {str(e)}")
        APIUsageStats.increment_call('reverse_geocode', success=False)
        return None
    except Exception as e:
        logger.error(f"逆地理编码请求失败 - 坐标: ({lng}, {lat}), 错误: {str(e)}", exc_info=True)
        APIUsageStats.increment_call('reverse_geocode', success=False)
        return None


def get_client_ip(request):
    """
    获取客户端真实IP地址
    
    处理代理服务器情况，优先获取X-Forwarded-For头中的IP，
    如果没有则获取REMOTE_ADDR。
    
    Args:
        request: HTTP请求对象
    
    Returns:
        str: 客户端IP地址
    """
    # 记录完整的request信息用于调试
    # logger.debug(f"Request 信息: {dict(request)}")

    # 记录完整的request.META信息用于调试
    # logger.debug(f"Request META信息: {dict(request.META)}")
    # logger.debug(f"Request META信息: {dict(request.META)}")

    # # 以JSON格式展示request.META信息
    # import json
    # meta_json = json.dumps(dict(request.META), ensure_ascii=False, indent=4)
    # logger.debug(f"Request META信息json格式: {meta_json}")

    # 记录请求的基本信息
    logger.debug(
        f"Request信息 - 方法: {request.method}, 路径: {request.path}, 内容类型: {getattr(request, 'content_type', 'unknown')}")

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # 记录X-Forwarded-For头部的值
    logger.debug(f"HTTP_X_FORWARDED_FOR头部值: {x_forwarded_for}")

    if x_forwarded_for:
        # 如果有代理，取第一个IP
        ip = x_forwarded_for.split(',')[0]
        logger.debug(f"从X-Forwarded-For获取到的IP: {ip}")
    else:
        # 直接连接，取REMOTE_ADDR
        ip = request.META.get('REMOTE_ADDR')
        logger.debug(f"从REMOTE_ADDR获取到的IP: {ip}")

    logger.info(f"最终获取到的客户端IP: {ip}")
    return ip


# 婚礼邀请首页视图函数
# 处理网站首页的HTTP请求并返回渲染后的模板
# 显示婚礼的基本信息、相册图片和访问统计
# 这是网站的主要入口页面
# 参数: request - Django HTTP请求对象
# 返回值: 渲染后的HttpResponse对象
def index(request):
    """
    婚礼邀请首页视图
    
    显示婚礼的基本信息、相册图片和访问统计。
    这是网站的主要入口页面。
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的首页模板
    """
    # 获取客户端的真实IP地址
    logger.debug(f"获取客户端IP地址")
    client_ip = get_client_ip(request)
    # 记录首页访问请求
    logger.info(f"首页请求 - IP: {client_ip}")
    # 记录请求详细信息
    logger.debug(
        f"首页请求详细 - 方法: {request.method}, 路径: {request.path}, 用户代理: {request.META.get('HTTP_USER_AGENT', 'unknown')}")

    # 开始处理首页请求的主要逻辑
    try:
        # 获取第一个婚礼事件（通常只有一个）
        logger.debug("数据库操作 - 开始获取婚礼事件")
        # 执行数据库查询获取婚礼事件
        wedding_event = WeddingEvent.objects.first()
        # 记录获取到的婚礼事件信息
        logger.info(f"成功获取婚礼事件: {wedding_event.title if wedding_event else 'None'}")
        # 记录婚礼事件详细信息
        if wedding_event:
            logger.debug(
                f"婚礼事件详细信息 - ID: {wedding_event.id}, 标题: {wedding_event.title}, 日期: {wedding_event.event_date}")

        # 获取相册图片
        logger.debug("数据库操作 - 开始获取相册图片")
        # 执行数据库查询获取所有相册图片
        gallery_images = GalleryImage.objects.all()
        # 记录获取到的相册图片数量
        logger.info(f"成功获取相册图片，数量: {gallery_images.count()}")
        # 记录相册图片详细信息
        logger.debug(
            f"相册图片详细 - 总数: {gallery_images.count()}, 第一张图片: {'存在' if gallery_images.first() else '不存在'}")

        # 记录首页加载完成的信息
        logger.info(
            f"首页加载完成 - 婚礼事件: {wedding_event.title if wedding_event else 'None'}, 相册图片数量: {gallery_images.count()}")
        # 记录更详细的加载信息
        logger.debug(
            f"首页加载详细 - 客户端IP: {client_ip}, 婚礼事件存在: {bool(wedding_event)}, 相册图片存在: {gallery_images.exists()}")

        # 增加首页访问次数（如果表存在）
        logger.debug("开始处理首页访问统计")
        try:
            logger.debug("数据库操作 - 开始更新首页访问统计")
            # 调用PageVisit模型的increment_visit方法增加访问次数
            PageVisit.increment_visit('homepage')
            logger.debug("数据库操作 - 首页访问统计更新完成")
        except Exception as e:
            # 记录更新访问统计时发生的异常
            logger.warning(f"无法更新首页访问统计: {str(e)}")
            # 记录异常的详细信息
            logger.debug(f"更新访问统计异常 - 错误类型: {type(e).__name__}, 错误: {str(e)}")

        # 获取首页访问次数（如果表存在）
        logger.debug("开始获取首页访问统计")
        try:
            logger.debug("数据库操作 - 开始获取首页访问统计")
            # 查询数据库获取首页访问记录
            homepage_visits = PageVisit.objects.filter(page_name='homepage').first()
            # 获取访问次数，如果不存在则默认为0
            homepage_visit_count = homepage_visits.visit_count if homepage_visits else 0
            logger.debug(f"数据库操作 - 获取首页访问统计完成: {homepage_visit_count}")
            # 记录访问统计的详细信息
            logger.debug(f"访问统计详细 - 访问次数: {homepage_visit_count}, 记录存在: {bool(homepage_visits)}")
        except Exception as e:
            # 记录获取访问统计时发生的异常
            logger.warning(f"无法获取首页访问统计: {str(e)}")
            # 记录异常的详细信息
            logger.debug(f"获取访问统计异常 - 错误类型: {type(e).__name__}, 错误: {str(e)}")
            # 设置默认访问次数为0
            homepage_visit_count = 0
        # 记录最终访问次数
        logger.debug(f"最终首页访问次数: {homepage_visit_count}")

        # 构建模板上下文，用于传递数据给前端模板
        logger.debug("开始构建模板上下文")
        context = {
            'wedding_event': wedding_event,  # 婚礼事件数据
            'gallery_images': gallery_images,  # 相册图片数据
            'homepage_visit_count': homepage_visit_count,  # 首页访问次数
        }
        # 记录上下文构建完成
        logger.debug(f"模板上下文构建完成 - 数据项数量: {len(context)}")

        # 记录首页视图渲染完成的信息
        logger.info(
            f"首页视图渲染完成 - IP: {client_ip}, 婚礼事件: {bool(wedding_event)}, 相册图片数量: {gallery_images.count()}")
        # 记录更详细的渲染信息
        logger.debug(f"渲染详细信息 - 请求路径: {request.path}, 模板: index.html, 上下文数据项: {len(context)}")

        # 渲染并返回首页模板
        logger.debug("开始渲染首页模板")
        response = render(request, 'index.html', context)
        logger.debug("首页模板渲染完成")
        return response

    # 捕获处理首页请求时发生的所有异常
    except Exception as e:
        # 记录详细的错误信息，包括完整的堆栈跟踪
        logger.error(f"首页视图处理失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 记录异常的详细类型和信息
        logger.debug(f"异常详细 - 类型: {type(e).__name__}, 模块: {e.__class__.__module__}, 参数: {e.args}")
        # 即使出错也返回基本的响应，确保用户能看到页面
        logger.debug("构建错误恢复上下文")
        context = {
            'wedding_event': None,  # 无婚礼事件数据
            'gallery_images': [],  # 空的相册图片列表
            'homepage_visit_count': 0,  # 0访问次数
        }
        # 记录错误恢复上下文构建完成
        logger.debug(f"错误恢复上下文构建完成 - 数据项数量: {len(context)}")
        # 渲染错误恢复页面
        logger.debug("渲染错误恢复首页")
        response = render(request, 'index.html', context)
        logger.debug("错误恢复首页渲染完成")
        return response


def rsvp_form(request):
    """
    RSVP回复表单页面视图
    
    显示RSVP表单，让宾客可以回复是否参加婚礼。
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的RSVP表单页面
    """
    client_ip = get_client_ip(request)
    logger.info(f"RSVP表单页面请求 - IP: {client_ip}")

    try:
        # 获取最新的婚礼事件
        logger.debug("数据库操作 - 开始获取最新的婚礼事件")
        wedding_event = WeddingEvent.objects.order_by('-created_at').first()
        logger.info(f"RSVP页面加载 - 婚礼事件: {wedding_event.title if wedding_event else 'None'}")

        # 构建上下文
        context = {
            'wedding_event': wedding_event
        }

        logger.info(f"RSVP表单页面渲染完成 - IP: {client_ip}")
        return render(request, 'rsvp.html', context)

    except Exception as e:
        logger.error(f"RSVP表单页面加载失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 即使出错也返回基本的响应
        context = {
            'wedding_event': None
        }
        return render(request, 'rsvp.html', context)


@csrf_exempt # 目前使用了@csrf_exempt跳过CSRF验证，存在安全隐患;前端已经正确发送CSRF令牌，应该移除该装饰器增强安全性
@require_http_methods(["POST"])
def submit_rsvp(request):
    """
    提交RSVP回复
    
    Args:
        request: HTTP POST请求对象，包含RSVP数据
    
    Returns:
        JsonResponse: 包含提交结果的JSON响应
    """
    client_ip = get_client_ip(request)
    logger.info(f"提交RSVP请求 - IP: {client_ip}")

    try:
        # 解析请求体中的JSON数据
        logger.debug(f"解析请求体JSON数据 - IP: {client_ip}")
        data = json.loads(request.body)

        # 提取RSVP数据
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        invitation_code = data.get('invitation_code')
        rsvp_status = data.get('rsvp_status', False)
        guest_count = data.get('guest_count', 1)
        message = data.get('message', '')

        logger.info(
            f"收到RSVP数据 - 姓名: {name}, 邀请码: {invitation_code}, 出席状态: {rsvp_status}, 人数: {guest_count}")

        # 验证必要字段
        if not name or not invitation_code:
            logger.warning(f"RSVP数据验证失败 - 缺少必要字段 - IP: {client_ip}")
            return JsonResponse({
                'success': False,
                'message': '姓名和邀请码为必填项'
            })

        # 检查邀请码是否已存在
        logger.debug(f"数据库操作 - 检查邀请码是否已存在: {invitation_code}")
        if Guest.objects.filter(invitation_code=invitation_code).exists():
            logger.warning(f"邀请码已被使用 - IP: {client_ip}, 邀请码: {invitation_code}")
            return JsonResponse({
                'success': False,
                'message': '该邀请码已被使用'
            })

        # 创建新的宾客记录
        logger.info(f"数据库操作 - 开始创建新的宾客记录 - 姓名: {name}, 邀请码: {invitation_code}")
        guest = Guest.objects.create(
            name=name,
            phone=phone,
            email=email,
            invitation_code=invitation_code,
            rsvp_status=rsvp_status,
            guest_count=guest_count,
            message=message
        )
        logger.info(f"数据库操作 - 宾客记录创建成功 - ID: {guest.id}, 姓名: {guest.name}")

        logger.info(f"RSVP提交成功 - 宾客ID: {guest.id}, 姓名: {name}, 邀请码: {invitation_code}")

        return JsonResponse({
            'success': True,
            'message': 'RSVP提交成功，感谢您的回复！'
        })

    except json.JSONDecodeError as e:
        logger.error(f"RSVP JSON解析失败 - IP: {client_ip}, 错误: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'JSON格式错误'
        })
    except Exception as e:
        logger.error(f"RSVP提交失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'提交失败：{str(e)}'
        })


def countdown(request):
    """
    婚礼倒计时页面视图
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的倒计时页面
    """
    client_ip = get_client_ip(request)
    logger.info(f"倒计时页面请求 - IP: {client_ip}")

    try:
        # 获取最新的婚礼事件
        logger.debug("数据库操作 - 开始获取最新的婚礼事件")
        wedding_event = WeddingEvent.objects.order_by('-created_at').first()

        if wedding_event:
            # 计算距离婚礼还有多少天
            today = timezone.now().date()
            event_date = wedding_event.event_date.date()
            days_left = (event_date - today).days

            logger.info(f"倒计时计算 - 婚礼日期: {event_date}, 距离天数: {max(0, days_left)}")

            context = {
                'wedding_event': wedding_event,
                'days_left': max(0, days_left)
            }
        else:
            logger.warning("未找到婚礼事件")
            context = {
                'days_left': 0
            }

        logger.info(
            f"倒计时页面渲染完成 - IP: {client_ip}, 婚礼事件: {bool(wedding_event)}, 剩余天数: {context.get('days_left', 0)}")
        return render(request, 'countdown.html', context)

    except Exception as e:
        logger.error(f"倒计时页面加载失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 返回基本的错误页面
        context = {
            'days_left': 0
        }
        return render(request, 'countdown.html', context)


def gallery(request):
    """
    相册页面视图
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的相册页面
    """
    client_ip = get_client_ip(request)
    logger.info(f"相册页面请求 - IP: {client_ip}")

    try:
        # 获取按上传时间排序的相册图片
        logger.debug("数据库操作 - 开始获取相册图片")
        gallery_images = GalleryImage.objects.all().order_by('-uploaded_at')

        # 获取最新的婚礼事件
        logger.debug("数据库操作 - 开始获取最新的婚礼事件")
        wedding_event = WeddingEvent.objects.order_by('-created_at').first()

        logger.info(
            f"相册页面加载 - 相册图片数量: {gallery_images.count()}, 婚礼事件: {wedding_event.title if wedding_event else 'None'}")

        # 构建上下文
        context = {
            'gallery_images': gallery_images,
            'wedding_event': wedding_event
        }

        logger.info(f"相册页面渲染完成 - IP: {client_ip}, 图片数量: {gallery_images.count()}")
        return render(request, 'gallery.html', context)

    except Exception as e:
        logger.error(f"相册页面加载失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 即使出错也返回基本的响应
        context = {
            'gallery_images': [],
            'wedding_event': None
        }
        return render(request, 'gallery.html', context)


def ensure_gallery_directory():
    """
    确保相册目录存在
    """
    import os
    from django.conf import settings

    gallery_path = os.path.join(settings.MEDIA_ROOT, settings.GALLERY_UPLOAD_PATH)
    covers_path = os.path.join(settings.MEDIA_ROOT, settings.WEDDING_COVERS_UPLOAD_PATH)

    logger.info(f"检查相册目录是否存在 - 相册路径: {gallery_path}, 封面路径: {covers_path}")

    os.makedirs(gallery_path, exist_ok=True)
    os.makedirs(covers_path, exist_ok=True)

    logger.info("相册目录检查完成")


# 在应用启动时确保目录存在
ensure_gallery_directory()


# 地图位置页面视图函数
# 处理地图页面的HTTP请求并返回渲染后的模板
# 显示婚礼地点在地图上的位置
# 参数: request - Django HTTP请求对象
# 返回值: 渲染后的HttpResponse对象
def map_location(request):
    """
    地图位置页面视图
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的地图页面
    """
    # 获取客户端IP地址
    logger.debug("获取地图页面请求的客户端IP")
    client_ip = get_client_ip(request)
    # 记录地图位置页面访问请求
    logger.info(f"地图位置页面请求 - IP: {client_ip}")
    # 记录请求的详细信息
    logger.debug(
        f"地图请求详细 - 方法: {request.method}, 路径: {request.path}, 用户代理: {request.META.get('HTTP_USER_AGENT', 'unknown')}")

    # 开始处理地图页面请求的主要逻辑
    try:
        # 获取最新的婚礼事件
        logger.debug("数据库操作 - 开始获取最新的婚礼事件")
        # 执行数据库查询获取最新的婚礼事件
        wedding_event = WeddingEvent.objects.order_by('-created_at').first()

        # 记录地图页面加载信息
        logger.info(f"地图页面加载 - 婚礼事件: {wedding_event.title if wedding_event else 'None'}")
        # 记录婚礼事件详细信息
        if wedding_event:
            logger.debug(
                f"婚礼事件详细 - ID: {wedding_event.id}, 标题: {wedding_event.title}, 日期: {wedding_event.event_date}, 地址: {wedding_event.address}")

        # 准备地图配置参数
        logger.debug("开始准备地图配置参数")
        # 初始化地图配置参数，包含默认坐标、缩放级别和标记信息
        logger.debug("构建默认地图配置")
        map_config = {
            'center_lat': DEFAULT_CENTER_LAT,  # 默认北京天安门纬度
            'center_lng': DEFAULT_CENTER_LNG,  # 默认北京天安门经度
            'zoom': DEFAULT_MAP_ZOOM,  # 默认缩放级别
            'marker_title': '',  # 标记标题
            'marker_content': '',  # 标记内容
            'venue': '',  # 婚礼场地名称
            'address': '',  # 婚礼地址
            'coordinates_found': False,  # 默认标记为未找到坐标
            'confidence': 0,  # 匹配置信度
            'geocoding_details': {}  # 地理编码详细信息
        }
        # 记录地图配置初始化完成
        logger.debug(f"默认地图配置初始化完成 - 配置项数量: {len(map_config)}")

        # 记录API密钥信息用于调试
        logger.info(f"API密钥配置: {settings.AMAP_JS_API_KEY}")
        logger.info(f"安全密钥配置: {'已配置' if getattr(settings, 'AMAP_SECURITY_JS_CODE', '') else '未配置'}")

        # 检查是否存在婚礼事件和地址，如果有则进行地理编码
        logger.debug(
            f"检查婚礼事件和地址 - 事件存在: {bool(wedding_event)}, 地址存在: {bool(wedding_event and wedding_event.address) if wedding_event else False}")
        if wedding_event and wedding_event.address:
            # 记录尝试地理编码的信息
            logger.info(f"尝试地理编码婚礼地址: {wedding_event.address}")
            # 记录地理编码详细信息
            logger.debug(
                f"地理编码详细 - 事件ID: {wedding_event.id}, 地址: {wedding_event.address}, API密钥长度: {len(settings.AMAP_WEB_SERVICE_KEY) if settings.AMAP_WEB_SERVICE_KEY else 0}")
            # 尝试通过高德地图API获取精确坐标
            geocoding_result = geocode_address(wedding_event.address, settings.AMAP_WEB_SERVICE_KEY)

            # 检查地理编码结果
            if geocoding_result:
                # 更新地图配置为地理编码成功的结果
                map_config.update({
                    'center_lat': geocoding_result['latitude'],
                    'center_lng': geocoding_result['longitude'],
                    'coordinates_found': True,  # 成功获取到坐标
                    'confidence': geocoding_result['confidence'],  # 匹配置信度
                    'geocoding_details': geocoding_result  # 地理编码详细信息
                })
                # 记录地理编码成功的信息
                logger.info(
                    f"地理编码成功 - 坐标: ({geocoding_result['longitude']}, {geocoding_result['latitude']}), 置信度: {geocoding_result['confidence']}")
                # 记录成功详细信息
                logger.debug(
                    f"地理编码成功详细 - 地址: {wedding_event.address}, 纬度: {geocoding_result['latitude']}, 经度: {geocoding_result['longitude']}, 级别: {geocoding_result.get('level', 'unknown')}")
            else:
                # 记录地理编码失败的信息
                logger.warning(f"地理编码失败 - 地址: {wedding_event.address}, 使用默认坐标")
                # 记录失败详细信息
                logger.debug(
                    f"地理编码失败详细 - 事件ID: {wedding_event.id if wedding_event else 'None'}, 地址: {wedding_event.address if wedding_event else 'None'}")

            # 设置标记点信息
            logger.debug("设置地图标记点信息")
            map_config.update({
                'marker_title': wedding_event.venue or wedding_event.title,
                'marker_content': wedding_event.address,
                'venue': wedding_event.venue or wedding_event.title,
                'address': wedding_event.address,
            })
            # 记录标记信息设置完成
            logger.debug(f"标记信息设置完成 - 标题: {map_config['marker_title']}, 内容: {map_config['marker_content']}")
        else:
            # 记录未找到婚礼事件或地址的信息
            logger.info("未找到婚礼事件或地址，使用默认地图配置")
            # 记录未找到的详细信息
            logger.debug(
                f"未找到婚礼信息详细 - 事件存在: {bool(wedding_event)}, 地址存在: {bool(wedding_event and wedding_event.address) if wedding_event else False}")
            # 如果没有婚礼事件或地址，使用默认坐标，但标记为未找到特定坐标
            map_config.update({
                'marker_title': '婚礼地点',
                'marker_content': '请在管理后台设置婚礼地址',
                'venue': '',
                'address': ''
            })
            # 记录默认配置设置完成
            logger.debug("默认地图配置设置完成")

        # 构建传递给模板的上下文数据
        logger.debug("开始构建地图页面上下文")
        context = {
            'wedding_event': wedding_event,  # 婚礼事件数据
            'amap_api_key': settings.AMAP_JS_API_KEY,  # 高德地图API密钥
            'amap_security_js_code': getattr(settings, 'AMAP_SECURITY_JS_CODE', ''),  # 安全密钥，可选
            'map_config': map_config  # 地图配置数据
        }
        # 记录上下文构建完成
        logger.debug(f"地图页面上下文构建完成 - 数据项数量: {len(context)}")

        # 记录地图页面渲染完成的信息
        logger.info(
            f"地图页面渲染完成 - IP: {client_ip}, 婚礼事件: {bool(wedding_event)}, 坐标查找成功: {map_config['coordinates_found']}")
        # 记录详细的渲染信息
        logger.debug(
            f"地图渲染详细 - 客户端IP: {client_ip}, 婚礼事件存在: {bool(wedding_event)}, 坐标查找成功: {map_config['coordinates_found']}, 地图配置项数: {len(map_config)}")

        # 渲染并返回地图页面
        logger.debug("开始渲染地图页面")
        response = render(request, 'map.html', context)
        logger.debug("地图页面渲染完成")
        return response

    # 捕获处理地图页面请求时发生的所有异常
    except Exception as e:
        # 记录详细的错误信息，包括完整的堆栈跟踪
        logger.error(f"地图页面加载失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 记录异常的详细类型和信息
        logger.debug(f"地图异常详细 - 类型: {type(e).__name__}, 模块: {e.__class__.__module__}, 参数: {e.args}")
        # 即使出错也返回基本的响应，确保用户能看到页面
        logger.debug("构建地图错误恢复上下文")
        # 异常情况下使用默认地图配置
        map_config = {
            'center_lat': DEFAULT_CENTER_LAT,
            'center_lng': DEFAULT_CENTER_LNG,
            'zoom': DEFAULT_MAP_ZOOM,
            'marker_title': '婚礼地点',
            'marker_content': '请在管理后台设置婚礼地址',
            'venue': '',
            'address': '',
            'coordinates_found': False
        }
        # 记录错误恢复配置构建完成
        logger.debug("地图错误恢复配置构建完成")

        # 记录异常情况下的API密钥信息
        logger.info(f"异常处理 - API密钥配置: {settings.AMAP_JS_API_KEY}")
        logger.info(
            f"异常处理 - 安全密钥配置: {'已配置' if getattr(settings, 'AMAP_SECURITY_JS_CODE', '') else '未配置'}")

        # 构建错误恢复上下文
        context = {
            'wedding_event': None,
            'amap_api_key': settings.AMAP_JS_API_KEY,
            'amap_security_js_code': getattr(settings, 'AMAP_SECURITY_JS_CODE', ''),  # 安全密钥，可选
            'map_config': map_config
        }
        # 记录错误恢复上下文构建完成
        logger.debug(f"地图错误恢复上下文构建完成 - 数据项数量: {len(context)}")
        # 渲染错误恢复页面
        logger.debug("渲染地图错误恢复页面")
        response = render(request, 'map.html', context)
        logger.debug("地图错误恢复页面渲染完成")
        return response


def guest_list(request):
    """
    宾客列表页面视图，显示所有确认出席的宾客信息
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的宾客列表页面
    """
    client_ip = get_client_ip(request)
    logger.info(f"宾客列表页面请求 - IP: {client_ip}")

    try:
        # 获取确认出席的宾客
        logger.debug("数据库操作 - 开始获取确认出席的宾客列表")
        attending_guests = Guest.objects.filter(rsvp_status=True).order_by('-created_at')

        # 计算统计信息
        logger.debug("开始计算宾客统计信息")
        total_guests_count = sum(guest.guest_count for guest in attending_guests)
        total_confirmed_guests = attending_guests.count()
        all_guests_count = Guest.objects.count()

        logger.info(
            f"宾客列表加载 - 确认出席人数: {total_confirmed_guests}, 预计总人数: {total_guests_count}, 总邀请人数: {all_guests_count}")

        # 增加宾客列表页面访问次数（如果表存在）
        try:
            logger.debug("数据库操作 - 开始更新宾客列表页面访问统计")
            PageVisit.increment_visit('guest_list_page')
            logger.debug("数据库操作 - 宾客列表页面访问统计更新完成")
        except Exception as e:
            logger.warning(f"无法更新宾客列表页面访问统计: {str(e)}")

        # 获取各页面访问次数（如果表存在）
        try:
            logger.debug("数据库操作 - 开始获取页面访问统计")
            homepage_visits = PageVisit.objects.filter(page_name='homepage').first()
            guest_list_visits = PageVisit.objects.filter(page_name='guest_list_page').first()

            homepage_visit_count = homepage_visits.visit_count if homepage_visits else 0
            guest_list_visit_count = guest_list_visits.visit_count if guest_list_visits else 0
            logger.debug(
                f"数据库操作 - 获取页面访问统计完成 - 首页访问: {homepage_visit_count}, 宾客列表访问: {guest_list_visit_count}")
        except Exception as e:
            logger.warning(f"无法获取页面访问统计: {str(e)}")
            homepage_visit_count = 0
            guest_list_visit_count = 0

        # 构建上下文
        context = {
            'attending_guests': attending_guests,
            'total_guests_count': total_guests_count,
            'total_confirmed_guests': total_confirmed_guests,
            'all_guests_count': all_guests_count,
            'homepage_visit_count': homepage_visit_count,
            'guest_list_visit_count': guest_list_visit_count,
        }

        logger.info(
            f"宾客列表页面渲染完成 - IP: {client_ip}, 确认出席人数: {total_confirmed_guests}, 预计总人数: {total_guests_count}")
        return render(request, 'guest_list.html', context)

    except Exception as e:
        logger.error(f"宾客列表页面加载失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 即使出错也返回基本的响应
        context = {
            'attending_guests': [],
            'total_guests_count': 0,
            'total_confirmed_guests': 0,
            'all_guests_count': 0,
            'homepage_visit_count': 0,
            'guest_list_visit_count': 0,
        }
        return render(request, 'guest_list.html', context)


def get_map_config(request):
    """
    地图配置API，返回地图初始化所需配置
    
    Args:
        request: HTTP请求对象
    
    Returns:
        JsonResponse: 包含地图配置信息的JSON响应
    """
    from django.conf import settings
    from django.http import JsonResponse
    from .models import WeddingEvent
    from django.core.serializers.json import DjangoJSONEncoder
    import json

    client_ip = get_client_ip(request)
    logger.info(f"地图配置API请求 - IP: {client_ip}")

    try:
        # 获取婚礼事件信息
        wedding_event = WeddingEvent.objects.first()

        # 默认配置
        map_config = {
            'center_lat': DEFAULT_CENTER_LAT,
            'center_lng': DEFAULT_CENTER_LNG,
            'zoom': 12,
            'marker_title': '婚礼地点',
            'marker_content': '请在管理后台设置婚礼地址',
            'coordinates_found': False,
            'confidence': 0,
            'geocoding_details': {}
        }

        # 如果有婚礼事件且地址存在，尝试获取地理编码
        if wedding_event and wedding_event.address:
            logger.info(f"尝试地理编码婚礼地址: {wedding_event.address}")
            # 尝试通过高德地图API获取精确坐标
            geocoding_result = geocode_address(wedding_event.address, settings.AMAP_WEB_SERVICE_KEY)

            if geocoding_result:
                # 更新地图配置
                map_config.update({
                    'center_lat': geocoding_result['latitude'],
                    'center_lng': geocoding_result['longitude'],
                    'zoom': 15,
                    'marker_title': wedding_event.venue or wedding_event.title,
                    'marker_content': wedding_event.address,
                    'coordinates_found': True,
                    'confidence': geocoding_result.get('confidence', 0),
                    'geocoding_details': geocoding_result
                })
            else:
                # 地理编码失败时使用默认配置
                map_config.update({
                    'marker_title': wedding_event.venue or wedding_event.title,
                    'marker_content': wedding_event.address,
                    'coordinates_found': False,
                    'confidence': 0,
                    'geocoding_details': {}
                })

        # 构建响应
        # 仅在开发环境下提供API密钥，生产环境应通过其他方式处理
        import os
        debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'

        response_data = {
            'success': True,
            'map_config': map_config,
            'has_security_code': bool(getattr(settings, 'AMAP_SECURITY_JS_CODE', '')),
            # 仅在调试模式下提供JS API密钥，生产环境应使用服务器代理等方式
            'js_api_key': getattr(settings, 'AMAP_JS_API_KEY', '') if debug_mode else '',
        }

        logger.info(
            f"地图配置API响应 - 婚礼事件: {bool(wedding_event)}, 坐标查找成功: {map_config['coordinates_found']}")
        return JsonResponse(response_data)

    except Exception as e:
        logger.error(f"地图配置API处理失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        error_response = {
            'success': False,
            'error': '配置获取失败',
            'message': str(e)
        }
        return JsonResponse(error_response, status=500)


def guest_stats_api(request):
    """
    宾客统计API，返回实时统计信息
    
    Args:
        request: HTTP请求对象
    
    Returns:
        JsonResponse: 包含宾客统计信息的JSON响应
    """
    client_ip = get_client_ip(request)
    logger.info(f"宾客统计API请求 - IP: {client_ip}")

    try:
        # 计算统计信息
        logger.debug("数据库操作 - 开始计算宾客统计信息")
        confirmed_guests = Guest.objects.filter(rsvp_status=True)
        total_confirmed_count = sum(guest.guest_count for guest in confirmed_guests)
        total_confirmed_people = confirmed_guests.count()
        total_invited = Guest.objects.count()
        pending_responses = Guest.objects.filter(rsvp_status=False).count()
        logger.debug(
            f"数据库操作 - 宾客统计信息计算完成 - 确认出席: {total_confirmed_count}, 确认人数: {total_confirmed_people}, 总邀请: {total_invited}, 待回复: {pending_responses}")

        # 构建统计信息响应
        stats = {
            'total_confirmed_count': total_confirmed_count,
            'total_confirmed_people': total_confirmed_people,
            'total_invited': total_invited,
            'pending_responses': pending_responses,
        }

        logger.info(
            f"宾客统计API响应 - 已确认人数: {total_confirmed_count}, 已确认宾客: {total_confirmed_people}, 总邀请: {total_invited}, 待回复: {pending_responses}")

        return JsonResponse(stats)

    except Exception as e:
        logger.error(f"宾客统计API处理失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 返回错误响应
        error_response = {
            'error': '统计信息获取失败',
            'message': str(e)
        }
        return JsonResponse(error_response, status=500)
