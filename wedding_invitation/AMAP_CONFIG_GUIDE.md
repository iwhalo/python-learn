# 高德地图API配置完整指南

## 目录

- [1. 申请API密钥和安全密钥](#1-申请api密钥和安全密钥)
  - [1.1 Web服务API密钥申请](#11-web服务api密钥申请)
- [2. 项目配置](#2-项目配置)
  - [2.1 环境变量配置（推荐）](#21-环境变量配置推荐)
  - [2.2 Settings.py 配置](#22-settingspy-配置)
  - [2.3 视图配置](#23-视图配置)
  - [2.4 前端配置](#24-前端配置)
- [3. 配置方式](#3-配置方式)
  - [3.1 开发环境配置](#31-开发环境配置)
  - [3.2 生产环境配置](#32-生产环境配置)
- [4. 验证配置](#4-验证配置)
- [5. 故障排除](#5-故障排除)
  - [5.1 常见错误](#51-常见错误)
  - [5.2 调试步骤](#52-调试步骤)
- [6. 地理编码API（地址转坐标）](#6-地理编码api地址转坐标)
  - [6.1 地理编码 API 服务地址](#61-地理编码-api-服务地址)
  - [6.2 请求参数](#62-请求参数)
  - [6.3 返回结果参数说明](#63-返回结果参数说明)
  - [6.4 地理编码匹配级别列表](#64-地理编码匹配级别列表)
- [7. 逆地理编码API（坐标转地址）](#7-逆地理编码api坐标转地址)
  - [7.1 逆地理编码 API 服务地址](#71-逆地理编码-api-服务地址)
  - [7.2 逆地理编码请求参数](#72-逆地理编码请求参数)
  - [7.3 逆地理编码返回结果参数说明](#73-逆地理编码返回结果参数说明)
  - [7.4 逆地理编码服务示例](#74-逆地理编码服务示例)
- [8. 项目中地理编码功能实现](#8-项目中地理编码功能实现)
  - [8.1 功能特性](#81-功能特性)
  - [8.2 技术实现](#82-技术实现)
  - [8.3 使用示例](#83-使用示例)
  - [8.4 置信度评估](#84-置信度评估)
  - [8.5 管理命令](#85-管理命令)
- [9. UI增强与用户体验](#9-ui增强与用户体验)
- [10. 管理功能](#10-管理功能)
- [11. 错误处理](#11-错误处理)
- [12. 注意事项](#12-注意事项)

## 1. 申请API密钥和安全密钥

1. 访问高德开放平台：https://lbs.amap.com/
2. 注册开发者账号并登录
3. 进入「控制台」-「应用管理」-「创建新应用」
4. 应用平台选择「Web端(JSAPI)」
5. 获取API Key和安全密钥(jscode)

### 1.1 Web服务API密钥申请

为了正常调用 Web 服务 API，请先注册成为高德开放平台开发者，并申请 Web 服务的 key。地理/逆地理编码 API 是通过 HTTP/HTTPS 协议访问远程服务的接口，提供结构化地址与经纬度之间的相互转化的能力。

**产品介绍**

地理编码/逆地理编码 API 提供以下能力：

- **地理编码**：将详细的结构化地址转换为高德经纬度坐标。且支持对地标性名胜景区、建筑物名称解析为高德经纬度坐标。
  - 结构化地址举例：北京市朝阳区阜通东大街6号转换后经纬度：116.480881,39.989410
  - 地标性建筑举例：天安门转换后经纬度：116.397499,39.908722

- **逆地理编码**：将经纬度转换为详细结构化的地址，且返回附近周边的 POI、AOI 信息。
  - 例如：116.480881,39.989410 转换地址描述后：北京市朝阳区阜通东大街6号

**结构化地址的定义**：

首先，地址肯定是一串字符，内含国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦等建筑物名称。按照由大区域名称到小区域名称组合在一起的字符。一个有效的地址应该是独一无二的。注意：针对大陆、港、澳地区的地理编码转换时可以将国家信息选择性的忽略，但省、市、城镇等级别的地址构成是不能忽略的。暂时不支持返回台湾省的详细地址信息。

**使用说明**

1. 申请【Web服务API】密钥（Key）
2. 拼接 HTTP 请求 URL，第一步申请的 Key 需作为必填参数一同发送
3. 接收 HTTP 请求返回的数据（JSON 或 XML 格式），解析数据

如无特殊声明，接口的输入参数和输出数据编码全部统一为 UTF-8。

## 2. 项目配置

### 2.1 环境变量配置（推荐）

创建 `.env` 文件（基于 `.env.example`）：

```bash
# 高德地图API密钥
AMAP_API_KEY=your_actual_api_key_here

# 高德地图安全密钥（JS API 2.0）
AMAP_SECURITY_JS_CODE=your_security_js_code_here

# Django设置
DEBUG=True
SECRET_KEY=your_secret_key_here
```

### 2.2 Settings.py 配置

项目已配置从环境变量获取API密钥和安全密钥：

```python
import os

# 高德地图API密钥
# 用于地理编码和地图展示功能
AMAP_API_KEY = os.environ.get('AMAP_API_KEY', '438b20ef7e326a90d2b6be7bf486c2e4')  # 从环境变量获取，如果不存在则使用默认值

# 高德地图安全密钥（可选，用于JS API 2.0）
AMAP_SECURITY_JS_CODE = os.environ.get('AMAP_SECURITY_JS_CODE', '')  # 从环境变量获取安全密钥
```

### 2.3 视图配置

地图视图已配置传递API密钥和安全密钥到前端：

```python
context = {
    'wedding_event': wedding_event,
    'amap_api_key': settings.AMAP_JS_API_KEY,
    'amap_security_js_code': getattr(settings, 'AMAP_SECURITY_JS_CODE', ''), # 安全密钥，可选
    'map_config': map_config
}
```

### 2.4 前端配置

前端使用官方推荐的AMapLoader加载方式：

```
<!-- 高德地图JS API 2.0 - 使用AMapLoader加载 -->
<script type="text/javascript">
    // 配置安全密钥（根据高德地图官方教程 - 推荐方式：静态安全密钥）
    window._AMapSecurityConfig = {
        securityJsCode: '{{ amap_security_js_code|default:"YOUR_JS_CODE_HERE" }}', // 请替换为你的安全密钥
    };
</script>
<script src="https://webapi.amap.com/loader.js"></script>
<script type="text/javascript">
    // 检查API密钥是否有效
    var apiKey = '{{ amap_api_key|default:"" }}';
    if (!apiKey || apiKey.trim() === '' || apiKey === '438b20ef7e326a90d2b6be7bf486c2e4') {
        console.warn('高德地图API密钥未配置或使用默认值，请在settings.py中配置有效的AMAP_API_KEY');
        // 显示警告信息给用户
        alert('高德地图API密钥未配置或使用默认值，请联系管理员配置有效的API密钥');
    }

    // 从服务端获取地图配置
    const mapConfig = {
        centerLat: parseFloat('{{ map_config.center_lat }}'),
        centerLng: parseFloat('{{ map_config.center_lng }}'),
        zoom: parseInt('{{ map_config.zoom }}'),
        markerTitle: "{{ map_config.marker_title|escapejs }}",
        markerContent: "{{ map_config.marker_content|escapejs }}",
        coordinatesFound: {{ map_config.coordinates_found|yesno:"true,false" }}
    };

    AMapLoader.load({
        key: apiKey, // 申请好的Web端开发者 Key，调用 load 时必填
        version: "2.0", // 指定要加载的 JS API 的版本，缺省时默认为 1.4.15
        plugins: ['AMap.ToolBar', 'AMap.Scale', 'AMap.OverView', 'AMap.MapType', 'AMap.Geolocation', 'AMap.GridLayer', 'AMap.Buildings', 'AMap.TileLayer.RoadNet'] // 预加载插件
    })
    .then((AMap) => {
        // 地图初始化代码...
    })
    .catch((e) => {
        console.error('高德地图加载失败:', e);
        const loadingElement = document.getElementById('map-loading');
        if (loadingElement) {
            loadingElement.innerHTML = '<p>地图加载失败: ' + e.message + '</p>';
        }
    });
</script>
```

## 3. 配置方式

### 3.1 开发环境配置

1. 在 `.env` 文件中填入你的API密钥和安全密钥
2. 确保环境变量已加载到项目中
3. 启动开发服务器

### 3.2 生产环境配置

#### 方式一：环境变量（推荐）

在生产服务器上设置环境变量：
```bash
export AMAP_API_KEY=your_production_api_key
export AMAP_SECURITY_JS_CODE=your_production_security_code
```

#### 方式二：代理服务器配置（最安全）

配置Nginx代理服务器：

```
server {
    listen       80;
    server_name  your-domain.com;  # 替换为你的域名

    # 自定义地图服务代理
    location /_AMapService/v4/map/styles {
        set $args "$args&jscode=您的安全密钥";
        proxy_pass https://webapi.amap.com/v4/map/styles;
    }
    
    # 海外地图服务代理
    location /_AMapService/v3/vectormap {
        set $args "$args&jscode=您的安全密钥";
        proxy_pass https://fmap01.amap.com/v3/vectormap;
    }
    
    # Web服务API 代理
    location /_AMapService/ {
        set $args "$args&jscode=您的安全密钥";
        proxy_pass https://restapi.amap.com/;
    }
}
```

然后在前端配置代理服务器：
```
window._AMapSecurityConfig = {
    serviceHost:'//your-domain.com/_AMapService',  // 替换为你的代理服务器地址
};
```

## 4. 验证配置

1. 启动项目后访问地图页面 (`/map/`)
2. 检查浏览器控制台是否有API相关的错误信息
3. 地图应能正常显示，包含道路名称、建筑物名称等详细信息
4. 检查网络面板，确认API请求正常

## 5. 故障排除

### 5.1 常见错误

- `INVALID_USER_KEY`: API密钥无效，请检查密钥是否正确
- `USER_KEY_RECYCLED`: API密钥已被回收，请重新申请
- `OVER_LIMIT`: API调用次数超限
- `USERKEY_PLAT_NOMATCH`: API密钥与平台类型不匹配

### 5.2 调试步骤

1. 检查API密钥是否正确配置
2. 检查安全密钥是否正确配置
3. 检查域名是否在高德平台中配置为合法域名
4. 检查网络连接是否正常

## 6. 地理编码API（地址转坐标）

地理编码 API 是通过 HTTP/HTTPS 协议访问远程服务的接口，提供将结构化地址转换为经纬度坐标的功能。适用于将详细的结构化地址转换为高德经纬度坐标，支持对地标性名胜景区、建筑物名称解析为高德经纬度坐标。

### 6.1 地理编码 API 服务地址

**URL**: `https://restapi.amap.com/v3/geocode/geo?parameters`

**请求方式**: `GET`

parameters 代表的参数包括必填参数和可选参数。所有参数均使用和号字符(&)进行分隔。

### 6.1 服务示例

```
https://restapi.amap.com/v3/geocode/geo?address=北京市朝阳区阜通东大街6号&output=XML&key=<用户的key>
```

| 参数 | 值 | 备注 |
|------|-----|------|
| address | 北京市朝阳区阜通东大街6号 | 填写结构化地址信息:省份城市区县城镇乡村街道门牌号码（必选）|
| city | 北京 | 查询城市，可选：城市中文、中文全拼、citycode、adcode（可选）|

**示例说明**: 
- address 是需要获取坐标的结构化地址
- output（XML）用于指定返回数据的格式
- Key 是用户请求数据的身份标识
- 详细参数说明请参考下方的请求参数说明

### 6.2 请求参数

| 参数名 | 含义 | 规则说明 | 是否必须 | 缺省值 |
|-------|------|----------|----------|--------|
| key | 高德Key | 用户在高德地图官网 申请 Web 服务 API 类型 Key | 必填 | 无 |
| address | 结构化地址信息 | 规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦，如：北京市朝阳区阜通东大街6号。 | 必填 | 无 |
| city | 指定查询的城市 | 可选输入内容包括：指定城市的中文（如北京）、指定城市的中文全拼（beijing）、citycode（010）、adcode（110000），不支持县级市。当指定城市查询内容为空时，会进行全国范围内的地址转换检索。adcode 信息可参考 城市编码表 获取 | 可选 | 无，会进行全国范围内搜索 |
| sig | 数字签名 | 请参考 数字签名获取和使用方法 | 可选 | 无 |
| output | 返回数据格式类型 | 可选输入内容包括：JSON，XML。设置 JSON 返回结果数据将会以 JSON 结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。 | 可选 | JSON |
| callback | 回调函数 | callback 值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效。 | 可选 | 无 |

### 6.3 返回结果参数说明

响应结果的格式可以通过请求参数 output 指定，默认为 JSON 形式。

以下是返回参数说明：

| 名称 | 含义 | 规则说明 |
|------|------|----------|
| status | 返回结果状态值 | 返回值为 0 或 1，0 表示请求失败；1 表示请求成功。|
| count | 返回结果数目 | 返回结果的个数。|
| info | 返回状态说明 | 当 status 为 0 时，info 会返回具体错误原因，否则返回"OK"。详情可以参阅 info 状态表|
| geocodes | 地理编码信息列表 | 结果对象列表，包括下述字段：|
| \|- country | 国家 | 国内地址默认返回中国|
| \|- province | 地址所在的省份名 | 例如：北京市。此处需要注意的是，中国的四大直辖市也算作省级单位。|
| \|- city | 地址所在的城市名 | 例如：北京市|
| \|- citycode | 城市编码 | 例如：010|
| \|- district | 地址所在的区 | 例如：朝阳区|
| \|- street | 街道 | 例如：阜通东大街|
| \|- number | 门牌 | 例如：6号|
| \|- adcode | 区域编码 | 例如：110101|
| \|- location | 坐标点 | 经度，纬度|
| \|- level | 匹配级别 | 参见下方的地理编码匹配级别列表|

**提示**: 部分返回值当返回值存在时，将以字符串类型返回；当返回值不存在时，则以数组类型返回。

### 6.4 地理编码匹配级别列表

| 匹配级别 | 示例 |
|----------|------|
| 国家 | 中国 |
| 省 | 河北省、北京市 |
| 市 | 宁波市 |
| 区县 | 北京市朝阳区 |
| 开发区 | 亦庄经济开发区 |
| 乡镇 | 回龙观镇 |
| 村庄 | 三元村 |
| 热点商圈 | 上海市黄浦区老西门 |
| 道路 | 北京市朝阳区阜通东大街 |
| 道路交叉路口 | 北四环西路辅路/善缘街 |
| 兴趣点 | 北京市朝阳区奥林匹克公园(南门) |
| 门牌号 | 朝阳区阜通东大街6号 |
| 单元号 | 望京西园四区5号楼2单元 |
| 楼层 | 保留字段，建议兼容 |
| 房间 | 保留字段，建议兼容 |
| 公交地铁站点 | 海淀黄庄站 A1西北口 |
| 门址（新增） | 北京市朝阳区阜荣街10号 |
| 小巷（新增） | 保留字段，建议兼容 |
| 住宅区（新增） | 广西壮族自治区柳州市鱼峰区德润路华润凯旋门 |
| 未知 | 未确认级别的 POI |

## 7. 逆地理编码API（坐标转地址）

逆地理编码 API 是通过 HTTP/HTTPS 协议访问远程服务的接口，提供将经纬度坐标转换为详细结构化地址的功能。适用于将经纬度转换为详细结构化的地址，且返回附近周边的 POI、AOI 信息。

### 7.1 逆地理编码 API 服务地址

**URL**: `https://restapi.amap.com/v3/geocode/regeo?parameters`

**请求方式**: `GET`

parameters 代表的参数包括必填参数和可选参数。所有参数均使用和号字符(&)进行分隔。

### 7.1 服务示例

```
https://restapi.amap.com/v3/geocode/regeo?location=116.481485,39.990464&output=JSON&key=<用户的key>
```

**示例说明**: 
- location 是需要获取地址信息的经纬度坐标
- output（JSON）用于指定返回数据的格式
- Key 是用户请求数据的身份标识
- 详细参数说明请参考下方的逆地理编码请求参数说明

### 7.2 逆地理编码请求参数

| 参数名 | 含义 | 规则说明 | 是否必须 | 缺省值 |
|-------|------|----------|----------|--------|
| key | 高德Key | 用户在高德地图官网 申请 Web 服务 API 类型 Key | 必填 | 无 |
| location | 经纬度坐标 | 传入内容规则：经度在前，纬度在后，经纬度间以","分割，经纬度小数点后不要超过 6 位。 | 必填 | 无 |
| poitype | 返回附近 POI 类型 | 以下内容需要 extensions 参数为 all 时才生效。逆地理编码在进行坐标解析之后不仅可以返回地址描述，也可以返回经纬度附近符合限定要求的 POI 内容（在 extensions 字段值为 all 时才会返回 POI 内容）。设置 POI 类型参数相当于为上述操作限定要求。参数仅支持传入 POI TYPECODE，可以传入多个 POI TYPECODE，相互之间用"|"分隔。获取 POI TYPECODE 可以参考 POI 分类码表 | 可选 | 无 |
| radius | 搜索半径 | radius 取值范围：0~3000，默认值：1000。单位：米 | 可选 | 1000 |
| extensions | 返回结果控制 | extensions 参数默认取值是 base，也就是返回基本地址信息；extensions 参数取值为 all 时会返回基本地址信息、附近 POI 内容、道路信息以及道路交叉口信息。 | 可选 | base |
| roadlevel | 道路等级 | 以下内容需要 extensions 参数为 all 时才生效。可选值：0，1 当 roadlevel=0时，显示所有道路 ； 当 roadlevel=1时，过滤非主干道路，仅输出主干道路数据 | 可选 | 无 |
| sig | 数字签名 | 请参考 数字签名获取和使用方法 | 可选 | 无 |
| output | 返回数据格式类型 | 可选输入内容包括：JSON，XML。设置 JSON 返回结果数据将会以 JSON 结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。 | 可选 | JSON |
| callback | 回调函数 | callback 值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效。 | 可选 | 无 |
| homeorcorp | 是否优化 POI 返回顺序 | 以下内容需要 extensions 参数为 all 时才生效。homeorcorp 参数的设置可以影响召回 POI 内容的排序策略，目前提供三个可选参数：0：不对召回的排序策略进行干扰。1：综合大数据分析将居家相关的 POI 内容优先返回，即优化返回结果中 pois 字段的poi 顺序。2：综合大数据分析将公司相关的 POI 内容优先返回，即优化返回结果中 pois 字段的poi 顺序。 | 可选 | 0 |

### 7.3 逆地理编码返回结果参数说明

逆地理编码的响应结果的格式由请求参数 output 指定。

以下是返回参数说明：

| 名称 | 含义 | 规则说明 |
|------|------|----------|
| status | 返回结果状态值 | 返回值为 0 或 1，0 表示请求失败；1 表示请求成功。|
| info | 返回状态说明 | 当 status 为 0 时，info 会返回具体错误原因，否则返回"OK"。详情可以参考 info 状态表 |
| regeocode | 逆地理编码列表 | 返回 regeocode 对象；regeocode 对象包含的数据如下： |
| \|- addressComponent | 地址元素列表 | |
| \|- \|- country | 坐标点所在国家名称 | 例如：中国 |
| \|- \|- province | 坐标点所在省名称 | 例如：北京市 |
| \|- \|- city | 坐标点所在城市名称 | 请注意：当城市是省直辖县时返回为空，以及城市为北京、上海、天津、重庆四个直辖市时，该字段返回为空；省直辖县列表 |
| \|- \|- citycode | 城市编码 | 例如：010 |
| \|- \|- district | 坐标点所在区 | 例如：海淀区 |
| \|- \|- adcode | 行政区编码 | 例如：110108 |
| \|- \|- township | 坐标点所在乡镇/街道（此街道为社区街道，不是道路信息） | 例如：燕园街道 |
| \|- \|- towncode | 乡镇街道编码 | 例如：110101001000 |
| \|- \|- neighborhood | 社区信息列表 | |
| \|- \|- \|- name | 社区名称 | 例如：北京大学 |
| \|- \|- \*- type | POI 类型 | 例如：科教文化服务;学校;高等院校 |
| \|- \|- building | 楼信息列表 | |
| \|- \*- \*- name | 建筑名称 | 例如：万达广场 |
| \|- \*- \*- type | 类型 | 例如：科教文化服务;学校;高等院校 |
| \|- \|- streetNumber | 门牌信息列表 | |
| \|- \*- \*- street | 街道名称 | 例如：中关村北二条 |
| \|- \*- \*- number | 门牌号 | 例如：3号 |
| \|- \*- location | 坐标点 | 经纬度坐标点：经度，纬度 |
| \|- \*- direction | 方向 | 坐标点所处街道方位 |
| \|- \*- distance | 门牌地址到请求坐标的距离 | 单位：米 |
| \|- \|- seaArea | 所属海域信息 | 例如：渤海 |
| \|- businessAreas | 经纬度所属商圈列表 | |
| \|- \|- businessArea | 商圈信息 | |
| \|- \*- \*- location | 商圈中心点经纬度 | |
| \|- \*- \*- name | 商圈名称 | 例如：颐和园 |
| \|- \*- \*- id | 商圈所在区域的 adcode | 例如：朝阳区/海淀区 |
| \|- roads | 道路信息列表 | 请求参数 extensions 为 all 时返回如下内容 |
| \|- \|- road | 道路信息 | |
| \|- \*- \*- id | 道路 id | |
| \|- \*- \*- name | 道路名称 | |
| \|- \*- \*- distance | 道路到请求坐标的距离 | 单位：米 |
| \|- \*- \*- direction | 方向 | 输入点和此路的相对方位 |
| \|- \*- \*- location | 坐标点 | |
| \|- roadinters | 道路交叉口列表 | 请求参数 extensions 为 all 时返回如下内容 |
| \|- \|- roadinter | 道路交叉口 | |
| \|- \*- \*- distance | 交叉路口到请求坐标的距离 | 单位：米 |
| \|- \*- \*- direction | 方向 | 输入点相对路口的方位 |
| \|- \*- \*- location | 路口经纬度 | |
| \|- \*- \*- first_id | 第一条道路 id | |
| \|- \*- \*- first_name | 第一条道路名称 | |
| \|- \*- \*- second_id | 第二条道路 id | |
| \|- \*- \*- second_name | 第二条道路名称 | |
| \|- pois | poi 信息列表 | 请求参数 extensions 为 all 时返回如下内容 |
| \|- \|- poi | poi 信息列表 | |
| \|- \|- \|- id | poi 的 id | |
| \|- \|- \|- name | poi 点名称 | |
| \|- \|- \|- type | poi 类型 | |
| \|- \|- \|- tel | 电话 | |
| \|- \|- \|- distance | 该 POI 的中心点到请求坐标的距离 | 单位：米 |
| \|- \|- \|- direction | 方向 | 相对于输入点的方位 |
| \|- \|- \|- address | poi 地址信息 | |
| \|- \|- \|- location | 坐标点 | |
| \|- \|- \|- businessarea | poi 所在商圈名称 | |
| \|- aois | aoi 信息列表 | 请求参数 extensions 为 all 时返回如下内容 |
| \|- \|- aoi | aoi 信息 | |
| \|- \*- \*- id | 所属 aoi 的 id | |
| \|- \*- \*- name | 所属 aoi 名称 | |
| \|- \*- \*- adcode | 所属 aoi 所在区域编码 | |
| \|- \*- \*- location | 所属 aoi 中心点坐标 | |
| \|- \*- \*- area | 所属 aoi 点面积 | 单位：平方米 |
| \|- \*- \*- distance | 输入经纬度是否在 aoi 面之中 | 0，代表在 aoi 内 其余整数代表距离 AOI 的距离 |
| \|- \*- \*- type | 所属 aoi 类型 | |

**提示**: 部分返回值当返回值存在时，将以字符串类型返回；当返回值不存在时，则以数组类型返回。

### 7.4 逆地理编码服务示例

```
https://restapi.amap.com/v3/geocode/regeo?output=xml&location=116.310003,39.991957&key=<用户的key>&radius=1000&extensions=all
```

| 参数 | 值 | 备注 |
|------|-----|------|
| location | 116.481488,39.990464 | 经纬度坐标（必选）|
| poitype | 商务写字楼 | 支持传入 POI TYPECODE 及名称；支持传入多个 POI 类型，多值间用"|"分隔（可选）|
| radius | 1000 | 查询 POI 的半径范围。取值范围：0~3000,单位：米（可选）|
| extensions | all | 返回结果控制（可选）|
| roadlevel | 0 | 可选值：1，当 roadlevel=1时，过滤非主干道路，仅输出主干道路数据（可选）|

**说明**: 
- location(116.310003,39.991957) 是所需要转换的坐标点经纬度
- radius（1000）为返回的附近 POI 的范围，单位：米
- extensions(all)为返回的数据内容
- output（XML）用于指定返回数据的格式
- Key 是高德 Web 服务 Key
- 详细可以参考上方的请求参数说明

## 8. 项目中地理编码功能实现

本项目实现了完整的地理编码功能，包括以下特性：

### 8.1 功能特性

- **完整API参数支持**：支持所有高德地图地理编码API参数（key, address, city, sig, output, callback）
- **逆地理编码功能**：实现坐标转地址的逆向转换功能
- **置信度评估机制**：根据匹配级别计算置信度分数
- **缓存机制**：避免重复API调用，提升性能
- **API限制管理**：跟踪调用次数，防止超出配额
- **错误处理**：完善的异常捕获和错误日志记录

### 8.2 技术实现

#### 8.2.1 核心函数

1. `geocode_address()`：地理编码函数，支持全部API参数
   - 参数：address（地址）, api_key（API密钥）, city（城市）, sig（签名）, output（输出格式）, callback（回调函数）, use_cache（是否使用缓存）, daily_limit（每日限制）
   - 返回：包含经纬度、地址信息、置信度等的字典

2. `reverse_geocode()`：逆地理编码函数
   - 参数：lat（纬度）, lng（经度）, api_key（API密钥）, extensions（扩展信息）, use_cache（是否使用缓存）, daily_limit（每日限制）
   - 返回：包含详细地址信息的字典

3. `calculate_confidence()`：置信度计算函数
   - 根据匹配级别计算1-5分的置信度

#### 8.2.2 数据模型

1. `GeocodingCache`：地理编码缓存模型
   - 缓存地址查询结果，避免重复API调用
   - 支持自动过期清理

2. `APIUsageStats`：API使用统计模型
   - 跟踪每日API调用次数
   - 统计成功和失败次数
   - 支持调用限制检查

### 8.3 使用示例

```
# 地理编码调用示例
result = geocode_address(
    address="北京市朝阳区阜通东大街6号",
    api_key=settings.AMAP_API_KEY,
    city="北京",
    use_cache=True,
    daily_limit=1000
)

# 逆地理编码调用示例
result = reverse_geocode(
    lat=39.997213,
    lng=116.481938,
    api_key=settings.AMAP_API_KEY,
    extensions='all',
    use_cache=True,
    daily_limit=1000
)
```

### 8.4 置信度评估

根据匹配级别计算置信度：
- 门牌号、兴趣点：5分（最高）
- 交叉口、道路：4分（高）
- 区县、乡镇：3分（中）
- 地级市：2分（低）

### 8.5 管理命令

- `python manage.py cleanup_geocoding_cache`：清理过期缓存
- `python manage.py show_api_stats`：查看API使用统计

## 9. UI增强与用户体验

- 在地图页面显示置信度可视化指示器
- 显示地理编码详细信息
- 提供错误状态提示
- 增强用户体验

## 10. 管理功能

- 查看API使用统计
- 清理过期缓存
- 干运行模式支持

## 11. 错误处理

- 完善的异常捕获机制
- 详细的错误日志记录
- API密钥有效性检查
- 网络错误处理

## 12. 注意事项

- 2021年12月2日之后申请的API Key必须配合安全密钥使用
- API密钥请勿在公共仓库中暴露
- 生产环境建议使用代理服务器方式配置安全密钥
- 开发环境可使用静态安全密钥方式进行配置
- 项目已支持后端传递安全密钥，推荐使用这种方式
- 确保申请的API密钥类型为「Web端(JSAPI)」
- 详细的服务调用量限制可查阅高德开放平台官方文档
- 地理编码API和逆地理编码API有独立的调用限制，请合理规划使用量
- 城市编码(citycode)和区域编码(adcode)信息已提供工具支持，可参考map_data.city_code_utils模块
- POI分类编码信息已提供工具支持，可参考map_data.poi_utils模块
- 所有地图数据功能都集中在 `map_data` 包中，便于统一管理和维护
