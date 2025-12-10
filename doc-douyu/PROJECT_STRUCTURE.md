# 斗鱼文档抓取器项目结构

## 项目概述
这是一个用于抓取斗鱼文档（doc.douyu.tv）页面内容的Python工具。它能够获取文档内容、用户信息、附件、收藏状态和订阅状态等数据。

## 文件结构

```
doc-douyu/
├── __main__.py          # 主程序入口，可以直接运行
├── scraper.py           # 核心抓取器模块
├── test_scraper.py      # 测试脚本
├── install_and_run.py   # 安装依赖并运行的便捷脚本
├── requirements.txt     # 项目依赖
├── README.md           # 项目说明文档
├── PROJECT_STRUCTURE.md # 项目结构说明
├── api/                # API接口信息目录（包含HAR文件）
│   └── doc.douyu.tv.har
└── output/             # 输出目录（运行后创建）
    ├── doc_{id}_full_data.json    # 完整数据JSON文件
    ├── doc_{id}_content.txt       # 文档内容文本文件
    └── doc_{id}_info.json         # 文档信息JSON文件
```

## 核心功能模块

### 1. scraper.py - 核心抓取器
- `DouyuDocScraper` 类提供了完整的抓取功能
- 支持多个API端点的调用
- 提供内容保存和摘要生成功能

### 2. 主要API端点
- `/v1/api/doc/getDoc` - 获取文档内容
- `/v1/api/user/getUserInfo` - 获取用户信息
- `/v1/api/doc/getAttachment` - 获取附件
- `/v1/api/square/checkCollect` - 检查收藏状态
- `/v1/api/doc/checkSubscribe` - 检查订阅状态

### 3. 功能特性
- 从URL自动提取文档ID和空间ID
- 完整的文档内容抓取
- 用户信息获取
- 附件信息获取
- 收藏和订阅状态检查
- 内容摘要生成
- 数据保存到多种格式

## 使用方法

### 1. 直接运行
```bash
python -m doc-douyu
```

### 2. 通过模块运行
```bash
python scraper.py
```

### 3. 使用便捷安装脚本
```bash
python install_and_run.py
```

## 输出格式

抓取完成后，工具会生成以下格式的输出文件：

1. **JSON格式** - 包含完整的原始API响应数据
2. **TXT格式** - 纯文档内容，便于阅读和处理
3. **JSON摘要** - 文档基本信息，便于快速查看

## 技术特点

- 使用 `requests` 库进行HTTP请求
- 模拟浏览器请求头以绕过基本检测
- 支持多种数据格式输出
- 提供详细的错误处理和日志记录
- 模块化设计，易于扩展和维护