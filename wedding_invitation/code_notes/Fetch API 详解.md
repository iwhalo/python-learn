# Fetch API 详解

## 什么是 Fetch API？

Fetch API 是现代浏览器提供的一种**异步网络请求接口**，用于替代传统的 XMLHttpRequest (XHR) API，提供更简洁、更强大的网络请求能力。它基于 Promise 设计，支持异步编程模式，使网络请求代码更易读、易维护。

## Fetch API 的核心特性

1. **基于 Promise**：天然支持 Promise，可与 async/await 语法结合使用
2. **简洁的 API**：比 XMLHttpRequest 更简洁直观
3. **流式处理**：支持请求和响应的流式处理
4. **跨域支持**：内置对 CORS (跨源资源共享) 的支持
5. **灵活的请求配置**：可配置请求方法、头信息、请求体等
6. **响应类型处理**：内置多种响应类型解析方法（json、text、blob 等）

## Fetch API 的基本语法

```javascript
fetch(url, options)
  .then(response => {
    // 处理响应
  })
  .catch(error => {
    // 处理错误
  });
```

或使用 async/await 语法：

```javascript
async function fetchData() {
  try {
    const response = await fetch(url, options);
    // 处理响应
  } catch (error) {
    // 处理错误
  }
}
```

## 项目中的实际应用

在我们的婚礼邀请项目中，rsvp.html 文件使用 Fetch API 处理表单提交：

```javascript
try {
  // 发送POST请求到服务器
  const response = await fetch('/submit-rsvp/', {
    method: 'POST',  // 请求方法
    headers: {
      'Content-Type': 'application/json',  // 请求体格式
      'X-CSRFToken': getCookie('csrftoken')  // CSRF令牌，防止跨站请求伪造
    },
    body: JSON.stringify(data)  // 请求体数据（JSON格式）
  });
  
  // 解析响应数据
  const result = await response.json();
  
  // 处理解析后的结果
  if (result.success) {
    messageContainer.innerHTML = `<div class="message success">${result.message}</div>`;
    this.reset(); // 重置表单
    loadStats(); // 更新统计信息
  } else {
    messageContainer.innerHTML = `<div class="message error">${result.message}</div>`;
  }
} catch (error) {
  console.error('Error:', error);
  document.getElementById('messageContainer').innerHTML = '<div class="message error">提交失败，请稍后重试</div>';
}
```

## Fetch API 的主要配置选项

### 1. 请求方法（method）
- `GET`: 获取资源（默认）
- `POST`: 提交数据
- `PUT`: 更新资源
- `DELETE`: 删除资源
- `PATCH`: 部分更新资源
- 其他：`HEAD`, `OPTIONS`, `CONNECT`, `TRACE`

### 2. 请求头（headers）
用于设置请求的元信息，如：
- `Content-Type`: 请求体的媒体类型（JSON、表单数据等）
- `Authorization`: 认证信息
- `X-CSRFToken`: CSRF 令牌

### 3. 请求体（body）
发送给服务器的数据，可以是：
- 字符串（JSON.stringify(data)）
- FormData 对象
- Blob 对象
- ArrayBuffer 对象

### 4. 其他配置
- `mode`: 请求模式（`cors`, `no-cors`, `same-origin`）
- `credentials`: 凭证选项（`omit`, `same-origin`, `include`）
- `cache`: 缓存模式（`default`, `no-store`, `reload`, `no-cache`, `force-cache`）
- `signal`: AbortSignal 对象，用于取消请求

## 响应处理

Fetch API 的 `fetch()` 方法返回一个 Promise，解析为 Response 对象。Response 对象提供了多种方法来解析响应体：

### 1. json()
将响应体解析为 JSON 格式：
```javascript
const data = await response.json();
```

### 2. text()
将响应体解析为文本：
```javascript
const text = await response.text();
```

### 3. blob()
将响应体解析为 Blob（二进制大对象）：
```javascript
const blob = await response.blob();
```

### 4. arrayBuffer()
将响应体解析为 ArrayBuffer：
```javascript
const buffer = await response.arrayBuffer();
```

### 5. formData()
将响应体解析为 FormData 对象：
```javascript
const formData = await response.formData();
```

## 错误处理

Fetch API 的错误处理需要注意以下几点：

1. **网络错误**：当网络连接失败时，Promise 会被 reject
2. **HTTP 错误状态**：即使服务器返回 404、500 等错误状态码，Promise 仍然会被 resolve
3. **需要手动检查状态**：应使用 `response.ok` 或 `response.status` 来检查请求是否成功

```javascript
const response = await fetch(url);
if (!response.ok) {
  throw new Error(`HTTP error! status: ${response.status}`);
}
const data = await response.json();
```

## 安全性考虑

1. **CSRF 保护**：在提交表单时，应包含 CSRF 令牌
   ```javascript
   headers: {
     'X-CSRFToken': getCookie('csrftoken')
   }
   ```

2. **CORS 处理**：了解并正确配置跨域资源共享策略

3. **请求超时**：设置请求超时，避免请求长时间阻塞
   ```javascript
   // 使用 AbortSignal 设置超时
   const controller = new AbortController();
   const timeoutId = setTimeout(() => controller.abort(), 5000);
   
   const response = await fetch(url, {
     signal: controller.signal
   });
   clearTimeout(timeoutId);
   ```

4. **数据验证**：在客户端和服务器端都应验证数据

## 项目中的完整流程

在婚礼邀请项目中，Fetch API 的完整工作流程如下：

1. **表单提交**：用户填写并提交 RSVP 表单
2. **数据准备**：JavaScript 收集表单数据并进行类型转换
3. **发送请求**：使用 Fetch API 发送 POST 请求到 `/submit-rsvp/` 端点
4. **服务器处理**：Django 视图函数 `submit_rsvp` 接收并处理请求
5. **响应处理**：前端解析 JSON 响应并根据结果显示消息
6. **界面更新**：显示成功/错误消息，重置表单，更新统计信息

## 与 XMLHttpRequest 的对比

| 特性 | Fetch API | XMLHttpRequest |
|------|-----------|----------------|
| API 风格 | 现代、简洁、基于 Promise | 传统、回调风格 |
| 语法 | 更简洁、易读 | 繁琐、多层嵌套 |
| 异步支持 | 原生支持 Promise 和 async/await | 需要手动封装 Promise |
| 流式处理 | 支持 | 有限支持 |
| 错误处理 | 更清晰的错误处理机制 | 复杂的错误处理 |
| 浏览器支持 | 现代浏览器支持 | 所有主流浏览器支持 |

## 浏览器兼容性

Fetch API 支持所有现代浏览器（Chrome 42+, Firefox 39+, Safari 10.1+, Edge 14+）。对于旧版浏览器，可以使用 polyfill（如 `whatwg-fetch`）来提供支持。

## 优化建议

1. **添加超时处理**：防止请求长时间阻塞
   ```javascript
   const controller = new AbortController();
   const timeout = setTimeout(() => controller.abort(), 10000); // 10秒超时
   
   try {
     const response = await fetch(url, { signal: controller.signal });
     clearTimeout(timeout);
     // 处理响应
   } catch (error) {
     if (error.name === 'AbortError') {
       console.error('请求超时');
     } else {
       console.error('请求失败:', error);
     }
   }
   ```

2. **验证响应状态**：确保请求成功
   ```javascript
   const response = await fetch(url);
   if (!response.ok) {
     throw new Error(`请求失败: ${response.status} ${response.statusText}`);
   }
   ```

3. **优化请求头**：根据实际需要设置请求头，避免不必要的信息

4. **使用适当的缓存策略**：根据资源类型设置合适的缓存模式

## 总结

Fetch API 是现代 Web 开发中处理网络请求的首选 API，它提供了简洁、强大的网络请求能力，基于 Promise 设计，支持异步编程模式。在我们的婚礼邀请项目中，Fetch API 被用于处理 RSVP 表单提交，实现了前端与后端的异步通信，提供了良好的用户体验。

通过合理使用 Fetch API 的各种配置选项和响应处理方法，可以构建出高效、安全、可靠的网络请求系统。
