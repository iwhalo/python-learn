# 相册图片配置说明

## 目录结构

此项目包含以下与相册相关的目录配置：

- **媒体文件根目录**: `media/`
- **相册图片目录**: `media/gallery/` 
- **婚礼封面图片目录**: `media/wedding_covers/`

## 配置详情

在 `wedding_invitation/settings.py` 中定义了以下配置：

```python
# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 相册图片配置
GALLERY_UPLOAD_PATH = 'gallery/'
WEDDING_COVERS_UPLOAD_PATH = 'wedding_covers/'
```

## 管理命令

运行以下命令来确保相册目录存在：

```bash
python manage.py setup_gallery
```

## 使用方法

### 1. 上传相册图片

相册图片会自动上传到 `media/gallery/` 目录下。

### 2. 上传婚礼封面图片

婚礼封面图片会自动上传到 `media/wedding_covers/` 目录下。

### 3. 数据库模型

相册图片通过 `GalleryImage` 模型管理，包含以下字段：

- `title`: 图片标题
- `image`: 图片文件（存储在 `gallery/` 目录下）
- `description`: 图片描述
- `uploaded_at`: 上传时间

## 访问相册页面

访问 `/gallery/` 路径即可查看所有相册图片。

## 注意事项

1. 确保 `media` 目录有适当的读写权限
2. 在生产环境中，建议配置Web服务器（如nginx）来直接服务媒体文件
3. 定期备份 `media` 目录以防止数据丢失