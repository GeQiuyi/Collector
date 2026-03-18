# Collector

跨平台稍后读收集器。在手机上一键收集微信公众号、小红书、知乎、B站等平台的内容，统一存储、搜索和回看。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`--host 0.0.0.0` 确保局域网内手机可以访问。

### 3. 访问

- 电脑浏览器：`http://localhost:8000`
- 手机浏览器（同一 WiFi）：`http://<电脑局域网IP>:8000`

### 4. 配置手机分享快捷方式

参见 [shortcuts/README.md](shortcuts/README.md) 配置 Android HTTP Shortcuts，实现分享面板一键收集。

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/collect` | 收集内容，body: `{"content": "链接或文本"}` |
| GET | `/api/resources` | 资源列表，支持 `?search=关键词&page=1&size=20` |
| DELETE | `/api/resources/{id}` | 删除单条资源 |

完整 API 文档：启动服务后访问 `http://localhost:8000/docs`

## 技术栈

- Python / FastAPI
- SQLite / SQLAlchemy
- Tailwind CSS / Alpine.js
