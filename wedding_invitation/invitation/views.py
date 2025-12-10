from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import logging
from .models import WeddingEvent, Guest, GalleryImage, PageVisit
import json
import os
import urllib.parse
import urllib.request

# 获取logger实例
logger = logging.getLogger('invitation')


def geocode_address(address, api_key):
    """
    使用高德地图API将地址转换为经纬度坐标
    
    Args:
        address (str): 需要地理编码的地址
        api_key (str): 高德地图API密钥
    
    Returns:
        tuple or None: 经纬度坐标元组 (lng, lat)，失败时返回None
    """
    if not api_key or api_key == 'YOUR_AMAP_API_KEY_HERE':
        logger.warning("高德地图API密钥未配置或使用默认值")
        return None
    
    logger.info(f"开始地理编码 - 地址: {address}")
    
    # 构造请求URL
    base_url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        'key': api_key,
        'address': address,
        'city': '全国'
    }
    
    try:
        # 编码URL参数
        logger.debug(f"编码地理编码请求参数 - 地址: {address}")
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{encoded_params}"
        
        logger.debug(f"发送地理编码请求 - URL: {full_url[:100]}...")
        
        # 发送请求
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        logger.debug(f"地理编码响应 - 状态: {data.get('status')}, 结果数: {len(data.get('geocodes', []))}")
        
        # 检查API密钥是否有效
        if data.get('info') == 'INVALID_USER_KEY':
            logger.error(f"高德地图API密钥无效 - 请检查您的API密钥配置")
            return None
        elif data.get('info') == 'USER_KEY_RECYCLED':
            logger.error(f"高德地图API密钥已被回收 - 请重新申请API密钥")
            return None
        elif data.get('info') == 'OVER_LIMIT':
            logger.warning(f"高德地图API调用次数超限 - 地址: {address}")
            return None
        elif data.get('info') == 'USERKEY_PLAT_NOMATCH':
            logger.error(f"高德地图API密钥与平台类型不匹配 - 请检查您申请的API密钥类型是否适用于Web服务 - 地址: {address}")
            return None
        
        # 解析结果
        if data['status'] == '1' and data['geocodes']:
            location = data['geocodes'][0]['location']
            lng, lat = location.split(',')
            logger.info(f"地理编码成功 - 地址: {address}, 坐标: ({lng}, {lat})")
            return float(lng), float(lat)
        else:
            error_info = data.get('info', 'Unknown error')
            logger.warning(f"地理编码失败 - 地址: {address}, 错误: {error_info}")
            return None
    except urllib.error.HTTPError as e:
        logger.error(f"地理编码HTTP错误 - 地址: {address}, 错误代码: {e.code}, 原因: {e.reason}")
        return None
    except urllib.error.URLError as e:
        logger.error(f"地理编码URL错误 - 地址: {address}, 错误: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"地理编码响应JSON解析失败 - 地址: {address}, 错误: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"地理编码请求失败 - 地址: {address}, 错误: {str(e)}", exc_info=True)
        return None


def get_client_ip(request):
    """
    获取客户端IP地址
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    """
    婚礼邀请首页视图
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的首页模板
    """
    # 获取客户端IP地址
    client_ip = get_client_ip(request)
    logger.info(f"首页请求 - IP: {client_ip}")
    
    try:
        # 获取第一个婚礼事件（通常只有一个）
        logger.debug("数据库操作 - 开始获取婚礼事件")
        wedding_event = WeddingEvent.objects.first()
        logger.info(f"成功获取婚礼事件: {wedding_event.title if wedding_event else 'None'}")
        
        # 获取相册图片
        logger.debug("数据库操作 - 开始获取相册图片")
        gallery_images = GalleryImage.objects.all()
        logger.info(f"成功获取相册图片，数量: {gallery_images.count()}")
        
        logger.info(f"首页加载完成 - 婚礼事件: {wedding_event.title if wedding_event else 'None'}, 相册图片数量: {gallery_images.count()}")
        
        # 增加首页访问次数（如果表存在）
        try:
            logger.debug("数据库操作 - 开始更新首页访问统计")
            PageVisit.increment_visit('homepage')
            logger.debug("数据库操作 - 首页访问统计更新完成")
        except Exception as e:
            logger.warning(f"无法更新首页访问统计: {str(e)}")
        
        # 获取首页访问次数（如果表存在）
        try:
            logger.debug("数据库操作 - 开始获取首页访问统计")
            homepage_visits = PageVisit.objects.filter(page_name='homepage').first()
            homepage_visit_count = homepage_visits.visit_count if homepage_visits else 0
            logger.debug(f"数据库操作 - 获取首页访问统计完成: {homepage_visit_count}")
        except Exception as e:
            logger.warning(f"无法获取首页访问统计: {str(e)}")
            homepage_visit_count = 0
        
        # 构建模板上下文
        context = {
            'wedding_event': wedding_event,
            'gallery_images': gallery_images,
            'homepage_visit_count': homepage_visit_count,
        }
        
        logger.info(f"首页视图渲染完成 - IP: {client_ip}, 婚礼事件: {bool(wedding_event)}, 相册图片数量: {gallery_images.count()}")
        
        return render(request, 'index.html', context)
    
    except Exception as e:
        logger.error(f"首页视图处理失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 即使出错也返回基本的响应
        context = {
            'wedding_event': None,
            'gallery_images': [],
            'homepage_visit_count': 0,
        }
        return render(request, 'index.html', context)


def rsvp_form(request):
    """
    RSVP回复表单页面视图
    
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


@csrf_exempt
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
        
        logger.info(f"收到RSVP数据 - 姓名: {name}, 邀请码: {invitation_code}, 出席状态: {rsvp_status}, 人数: {guest_count}")
        
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
        
        logger.info(f"倒计时页面渲染完成 - IP: {client_ip}, 婚礼事件: {bool(wedding_event)}, 剩余天数: {context.get('days_left', 0)}")
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
        
        logger.info(f"相册页面加载 - 相册图片数量: {gallery_images.count()}, 婚礼事件: {wedding_event.title if wedding_event else 'None'}")
        
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


def map_location(request):
    """
    地图位置页面视图
    
    Args:
        request: HTTP请求对象
    
    Returns:
        HttpResponse: 渲染后的地图页面
    """
    client_ip = get_client_ip(request)
    logger.info(f"地图位置页面请求 - IP: {client_ip}")
    
    try:
        # 获取最新的婚礼事件
        logger.debug("数据库操作 - 开始获取最新的婚礼事件")
        wedding_event = WeddingEvent.objects.order_by('-created_at').first()
        
        logger.info(f"地图页面加载 - 婚礼事件: {wedding_event.title if wedding_event else 'None'}")
        
        # 准备地图配置参数
        logger.debug("开始准备地图配置参数")
        map_config = {
            'center_lat': 39.90923,  # 默认北京天安门纬度
            'center_lng': 116.397428,  # 默认北京天安门经度
            'zoom': 15,
            'marker_title': '',
            'marker_content': '',
            'venue': '',
            'address': '',
            'coordinates_found': False  # 默认标记为未找到坐标
        }
        
        if wedding_event and wedding_event.address:
            logger.info(f"尝试地理编码婚礼地址: {wedding_event.address}")
            # 尝试通过高德地图API获取精确坐标
            coordinates = geocode_address(wedding_event.address, settings.AMAP_API_KEY)
            
            if coordinates:
                lng, lat = coordinates
                map_config.update({
                    'center_lat': lat,
                    'center_lng': lng,
                    'coordinates_found': True  # 成功获取到坐标
                })
                logger.info(f"地理编码成功 - 坐标: ({lng}, {lat})")
            else:
                logger.warning(f"地理编码失败 - 地址: {wedding_event.address}, 使用默认坐标")
            
            # 设置标记点信息
            map_config.update({
                'marker_title': wedding_event.venue or wedding_event.title,
                'marker_content': wedding_event.address,
                'venue': wedding_event.venue or wedding_event.title,
                'address': wedding_event.address,
            })
        else:
            logger.info("未找到婚礼事件或地址，使用默认地图配置")
            # 如果没有婚礼事件或地址，使用默认坐标，但标记为未找到特定坐标
            map_config.update({
                'marker_title': '婚礼地点',
                'marker_content': '请在管理后台设置婚礼地址',
                'venue': '',
                'address': ''
            })
        
        # 构建上下文
        context = {
            'wedding_event': wedding_event,
            'amap_api_key': settings.AMAP_API_KEY,
            'map_config': map_config
        }
        
        logger.info(f"地图页面渲染完成 - IP: {client_ip}, 婚礼事件: {bool(wedding_event)}, 坐标查找成功: {map_config['coordinates_found']}")
        return render(request, 'map.html', context)
    
    except Exception as e:
        logger.error(f"地图页面加载失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 即使出错也返回基本的响应
        map_config = {
            'center_lat': 39.90923,
            'center_lng': 116.397428,
            'zoom': 15,
            'marker_title': '婚礼地点',
            'marker_content': '请在管理后台设置婚礼地址',
            'venue': '',
            'address': '',
            'coordinates_found': False
        }
        context = {
            'wedding_event': None,
            'amap_api_key': settings.AMAP_API_KEY,
            'map_config': map_config
        }
        return render(request, 'map.html', context)


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
        
        logger.info(f"宾客列表加载 - 确认出席人数: {total_confirmed_guests}, 预计总人数: {total_guests_count}, 总邀请人数: {all_guests_count}")
        
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
            logger.debug(f"数据库操作 - 获取页面访问统计完成 - 首页访问: {homepage_visit_count}, 宾客列表访问: {guest_list_visit_count}")
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
        
        logger.info(f"宾客列表页面渲染完成 - IP: {client_ip}, 确认出席人数: {total_confirmed_guests}, 预计总人数: {total_guests_count}")
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
        logger.debug(f"数据库操作 - 宾客统计信息计算完成 - 确认出席: {total_confirmed_count}, 确认人数: {total_confirmed_people}, 总邀请: {total_invited}, 待回复: {pending_responses}")
        
        # 构建统计信息响应
        stats = {
            'total_confirmed_count': total_confirmed_count,
            'total_confirmed_people': total_confirmed_people,
            'total_invited': total_invited,
            'pending_responses': pending_responses,
        }
        
        logger.info(f"宾客统计API响应 - 已确认人数: {total_confirmed_count}, 已确认宾客: {total_confirmed_people}, 总邀请: {total_invited}, 待回复: {pending_responses}")
        
        return JsonResponse(stats)
    
    except Exception as e:
        logger.error(f"宾客统计API处理失败 - IP: {client_ip}, 错误: {str(e)}", exc_info=True)
        # 返回错误响应
        error_response = {
            'error': '统计信息获取失败',
            'message': str(e)
        }
        return JsonResponse(error_response, status=500)