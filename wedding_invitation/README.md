# 婚礼邀请电子请柬系统

这是一个基于Python和Django框架开发的婚礼邀请电子请柬系统，具有现代化的设计和丰富的功能。

## 功能特性

- **精美页面设计**: 使用现代CSS样式，响应式布局，适配各种设备
- **婚礼信息展示**: 展示婚礼时间、地点、新人姓名等信息
- **倒计时功能**: 实时显示距离婚礼还有多少天
- **RSVP回复**: 宾客可以确认出席并留下祝福
- **相册展示**: 展示婚纱照、订婚照等纪念照片，支持自定义相册配置
- **地图位置**: 显示婚礼举办地点及交通指南

## 技术栈

- **后端**: Python + Django
- **前端**: HTML5, CSS3, JavaScript
- **数据库**: SQLite (默认)
- **字体**: Google Fonts Noto Serif SC

## 项目结构

```
wedding_invitation/
├── manage.py
├── wedding_invitation/          # 项目配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── invitation/                  # 邀请应用
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── templates/                   # 模板文件
│   ├── index.html
│   ├── rsvp.html
│   ├── countdown.html
│   ├── gallery.html
│   └── map.html
├── static/                      # 静态文件
│   └── css/
│       └── style.css
├── db.sqlite3
└── populate_data.py
```

## 快速开始

1. **安装依赖**:
   ```bash
   pip install django
   ```

2. **运行数据库迁移**:
   ```bash
   python manage.py migrate
   ```

3. **创建超级用户** (可选):
   ```bash
   python manage.py createsuperuser
   ```

4. **填充演示数据**:
   ```bash
   python populate_data.py
   ```

5. **启动开发服务器**:
   ```bash
   python manage.py runserver
   ```

6. **访问网站**:
   打开浏览器访问 http://127.0.0.1:8000/

## 管理后台

访问 http://127.0.0.1:8000/admin/ 可以管理婚礼信息、宾客信息和相册内容。

## 自定义配置

您可以根据需要修改以下内容：

- 在Django管理后台中编辑婚礼信息
- 修改模板文件以调整页面布局
- 更换静态资源文件以定制样式
- 添加更多相册图片

## 部署说明

在生产环境中部署时，建议:

1. 使用PostgreSQL或MySQL替换SQLite
2. 配置静态文件服务
3. 设置适当的中间件和安全选项
4. 配置邮件服务以发送确认邮件

## 许可证

此项目仅供学习和参考使用。