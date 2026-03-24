# Collector Notion 同步实现

## 原理

收集时同时写入本地 SQLite 和 Notion 数据库，互为备���。

```
用户收集 → 本地 SQLite + Notion API
```

## 实现

### 1. Notion 客户端 (`app/notion.py`)
- `NotionClient` 类：封装 Notion API 调用
- `add_page()` 方法：创建数据库记录
- 从环境变量读取配置

### 2. 集成到收集流程 (`app/routers/collect.py`)
- 收集成功后异步调用 Notion API
- 错误不阻塞响应，本地保存优先

### 3. 配置 (`.env`)
```bash
NOTION_API_KEY=xxx          # Integration Secret
NOTION_DATABASE_ID=xxx      # 数据库 ID
NOTION_ENABLED=true         # 开关
```

## Notion 侧配置

1. 创建 Integration：https://www.notion.so/my-integrations
2. 创建 Database，添加列：Title, URL, Source, Summary, Tags
3. 连接 Integration 到 Database（Add connections）

## 字段映射

| Collector | Notion 类型 |
|-----------|-------------|
| title | title |
| url | url |
| source | select |
| summary | text |
| tags | multi-select |
