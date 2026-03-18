import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")

SOURCE_RULES: list[tuple[str, list[str]]] = [
    ("wechat", ["mp.weixin.qq.com"]),
    ("xiaohongshu", ["xhslink.com", "xiaohongshu.com"]),
    ("zhihu", ["zhihu.com", "zhuanlan.zhihu.com"]),
    ("bilibili", ["bilibili.com", "b23.tv"]),
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
        "Mobile/15E148 Safari/604.1"
    )
}

MAX_SUMMARY_LEN = 100


@dataclass
class ParseResult:
    url: str | None
    source: str
    title: str | None
    summary: str | None


def extract_url(text: str) -> str | None:
    match = URL_PATTERN.search(text)
    return match.group(0) if match else None


def identify_source(url: str | None) -> str:
    if not url:
        return "other"
    for source, domains in SOURCE_RULES:
        if any(domain in url for domain in domains):
            return source
    return "other"


def _truncate(text: str | None, limit: int) -> str | None:
    if not text:
        return None
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "…"


def fetch_metadata(url: str | None) -> tuple[str | None, str | None]:
    """Request the URL and extract title + description from HTML."""
    if not url:
        return None, None
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        title = None
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title = title_tag.string.strip()

        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title["content"].strip()

        description = None
        for attr in [
            {"property": "og:description"},
            {"name": "description"},
            {"name": "Description"},
        ]:
            tag = soup.find("meta", attrs=attr)
            if tag and tag.get("content"):
                description = tag["content"].strip()
                break

        return title, _truncate(description, MAX_SUMMARY_LEN)
    except Exception:
        return None, None


def parse(content: str) -> ParseResult:
    url = extract_url(content)
    source = identify_source(url)
    title, summary = fetch_metadata(url)

    if not title:
        title = _truncate(content, 50)
    if not summary:
        summary = _truncate(content, MAX_SUMMARY_LEN)

    return ParseResult(url=url, source=source, title=title, summary=summary)
