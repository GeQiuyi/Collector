# Collector

跨平台稍后读收集器。在手机上一键收集微信公众号、小红书、知乎、B站等平台的内容，统一存储、搜索和回看。

## 特性

- 📱 **跨平台收集** - 支持微信、知乎、B站、小红书等
- 🔄 **Notion 同步** - 可选同步到 Notion 数据库，数据更安全
- 🔍 **全文搜索** - 搜索标题和摘要内容
- 🏷️ **标签分类** - 自定义标签整理收集内容

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

## Notion 同步配���（可选）

启用 Notion 同步后，收集的内容会自动同步到 Notion 数据库，实现数据备份和多端访问。

### 1. 创建 Notion Integration

1. 访问 https://www.notion.so/my-integrations
2. 点击「New integration」
3. 填写名称（如 Collector），选��你的工作区
4. 记录 **Internal Integration Secret**

### 2. 创建 Notion 数据库

1. 在 Notion 中创建一个新的 Database
2. 添加以下列：
   - **Title**（标题，title 类型）
   - **URL**（链接，url 类型）
   - **Source**（来源，select 类型：知乎/B站/微信公众号/小红书/其他）
   - **Summary**（摘要，text 类型）
   - **Tags**（标签，multi-select 类型）

### 3. 连接 Integration 和数据库

1. 打开你创建的数据库
2. 点击右上角「...」→「Add connections」
3. 选择你创建的 Integration

### 4. 获取 Database ID

1. 打开数据库，复制 URL
2. URL 格式：`https://www.notion.so/{database_id}?v=xxx`
3. 复制中间的 **database_id**

### 5. 配置��境变量

复制 `.env.example` 为 `.env`，填写 Notion 配置：

```bash
NOTION_API_KEY=secret_xxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxx
NOTION_ENABLED=true
```

### 6. 测试同步

启动服务后，收集一条内容，检查 Notion 数据库是否新增记录。

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
