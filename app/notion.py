"""Notion API 客户端"""
import os
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Notion API 配置
NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


class NotionConfig:
    """Notion 配置"""

    def __init__(
        self, api_key: str, database_id: str, enabled: bool = True
    ):
        self.api_key = api_key
        self.database_id = database_id
        self.enabled = enabled

    @classmethod
    def from_env(cls) -> "NotionConfig":
        """从环境变量加载配置"""
        enabled = os.getenv("NOTION_ENABLED", "true").lower() == "true"
        if not enabled:
            return cls(api_key="", database_id="", enabled=False)

        api_key = os.getenv("NOTION_API_KEY", "")
        database_id = os.getenv("NOTION_DATABASE_ID", "")

        if not all([api_key, database_id]):
            logger.warning("Notion 配置不完整，同步功能将被禁用")
            return cls(api_key=api_key, database_id=database_id, enabled=False)

        return cls(api_key=api_key, database_id=database_id, enabled=True)


class NotionClient:
    """Notion API 客户端"""

    def __init__(self, config: NotionConfig):
        self.config = config
        self._headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        }

    async def add_page(
        self,
        title: str | None,
        url: str | None,
        source: str,
        summary: str | None,
        tags: list[str],
    ) -> bool:
        """
        添加页面到 Notion 数据库

        Args:
            title: 标题
            url: 链接
            source: 来源
            summary: 摘要
            tags: 标签列表

        Returns:
            是否添加成功
        """
        if not self.config.enabled:
            logger.debug("Notion 同步已禁用，跳过添加页面")
            return False

        # 构建页面属性
        properties = {}

        # 标题 (Title 类型)
        if title:
            properties["Title"] = {
                "title": [{"text": {"content": title}}]
            }

        # 链接 (Url 类型)
        if url:
            properties["URL"] = {"url": url}

        # 来源 (Select 类型)
        source_map = {
            "zhihu": "知乎",
            "bilibili": "B站",
            "wechat": "微信公众号",
            "xiaohongshu": "小红书",
            "other": "其他",
        }
        properties["Source"] = {
            "select": {"name": source_map.get(source, "其他")}
        }

        # 摘要 (Text 类型)
        if summary:
            properties["Summary"] = {"rich_text": [{"text": {"content": summary}}]}

        # 标签 (Multi-select 类型)
        if tags:
            properties["Tags"] = {
                "multi_select": [{"name": tag} for tag in tags if tag.strip()]
            }

        url = f"{NOTION_BASE_URL}/pages"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    headers=self._headers,
                    json={
                        "parent": {"database_id": self.config.database_id},
                        "properties": properties,
                    },
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Notion 添加页面成功: {title}")
                return True

        except httpx.HTTPStatusError as e:
            logger.error(f"Notion API HTTP 错误: {e.response.status_code} - {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"Notion 添加页面异常: {e}")
            return False


# 全局实例（懒加载）
_notion_client: NotionClient | None = None


def get_notion_client() -> NotionClient | None:
    """获取 Notion 客户端单例"""
    global _notion_client

    if _notion_client is None:
        config = NotionConfig.from_env()
        if not config.enabled:
            logger.info("Notion 同步未启用")
            return None
        _notion_client = NotionClient(config)

    return _notion_client
