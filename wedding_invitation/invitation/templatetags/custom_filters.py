import json
from django import template

register = template.Library()

@register.filter
def tojson(value):
    """
    将Python对象转换为JSON字符串，用于在JavaScript中安全使用
    """
    try:
        # 处理Django模型和其他复杂对象
        def serialize_object(obj):
            if hasattr(obj, '__dict__'):
                return str(obj)
            elif isinstance(obj, bool):
                return obj
            elif obj is None:
                return None
            else:
                return str(obj)
        
        return json.dumps(value, default=serialize_object, ensure_ascii=False)
    except Exception:
        # 如果序列化失败，返回空对象
        return json.dumps({})