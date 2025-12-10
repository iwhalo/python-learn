# 斗鱼文档内容抓取工具

一个用于抓取斗鱼文档（doc.douyu.tv）页面内容的Python工具。

## 功能特性

- 抓取斗鱼文档页面的完整内容
- 获取文档基本信息（标题、创建者、更新时间等）
- 获取文档附件信息
- 检查文档的收藏和订阅状态
- 将内容保存为JSON和文本文件
- 支持从URL直接抓取

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本使用

直接运行主程序抓取默认页面：

```bash
python -m doc-douyu
```

或者指定要抓取的URL：

```bash
python -m doc-douyu "https://doc.douyu.tv/ddse/preview/space/251381?sid=539"
```

### 2. 在代码中使用

```python
from scraper import DouyuDocScraper

# 创建抓取器实例
scraper = DouyuDocScraper()

# 从URL抓取内容
url = "https://doc.douyu.tv/ddse/preview/space/251381?sid=539"
content_data = scraper.scrape_from_url(url)

if content_data:
    # 保存内容到文件
    scraper.save_content_to_file(content_data)
    
    # 获取内容摘要
    summary = scraper.get_content_summary(content_data)
    print(summary)
```

## API接口说明

工具使用了以下斗鱼文档API：

- `GET /v1/api/doc/getDoc` - 获取文档内容
- `GET /v1/api/user/getUserInfo` - 获取用户信息
- `GET /v1/api/doc/getAttachment` - 获取附件
- `GET /v1/api/square/checkCollect` - 检查收藏状态
- `GET /v1/api/doc/checkSubscribe` - 检查订阅状态

## 输出文件

抓取完成后，会在 `output/` 目录生成以下文件：

- `doc_{id}_full_data.json` - 包含所有数据的完整JSON文件
- `doc_{id}_content.txt` - 纯文档内容文本文件
- `doc_{id}_info.json` - 文档基本信息JSON文件

## 注意事项

- 请合理使用此工具，遵守网站的使用条款
- 频繁请求可能导致IP被限制
- 某些需要登录或特殊权限的文档可能无法抓取