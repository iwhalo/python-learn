import requests

security_headers={
    'X-Content-Type-Options':'nosniff',
    'X-Frame-Options':'DENY',
    'X-XSS-Protection':'1;mode=block',
    'Strict-Transport-Security':'max-age=31536000;includeSubDomains',
    'Content-Security-Policy':"default-src 'self'",
    'Referer-Policy':'strict-origin-when-cross-origin'
}

session=requests.Session()
session.headers.update(security_headers)

# CSRF令牌处理
def fetch_with_csrf(url,session=None):
    """处理CSRF保护的表单提交"""
    s=session or requests.Session()

    # 1.获取包含CSRF令牌的页面
    response=s.get(url)

    # 2.从响应中提取CSRF令牌（示例使用简单正则，实际应使用 HTML 解析）
    import re
    csrf_token=re.search(r'name="csrf_token" value="(.+?)"',response.text)
    if csrf_token:
        csrf_token=csrf_token.group()
    else:
        raise ValueError('无法找到CSRF令牌')

    # 3.提交表单，包含CSRF令牌
    data={
        'username','user',
        'password','pass',
        'csrf_token',csrf_token
    }
    response=s.post(url,data=data)
    return response

# 使用示例
with requests.Session() as s:
    response=fetch_with_csrf('https://example.com/login',s)