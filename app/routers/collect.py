from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resource
from app.schemas import CollectRequest, ResourceOut
from app.parser import parse
from app.notion import get_notion_client

router = APIRouter()


@router.post("/collect", response_model=ResourceOut)
async def collect(req: CollectRequest, db: Session = Depends(get_db)):
    result = parse(req.content)

    tags_str = ",".join(t.strip() for t in req.tags if t.strip())

    resource = Resource(
        title=result.title,
        url=result.url,
        source=result.source,
        summary=result.summary,
        tags=tags_str,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)

    # 同步到 Notion（异步，不阻塞响应）
    notion_client = get_notion_client()
    if notion_client:
        try:
            await notion_client.add_page(
                title=result.title,
                url=result.url,
                source=result.source,
                summary=result.summary,
                tags=req.tags,
            )
        except Exception as e:
            # Notion 同步失败不影响本地保存
            print(f"Notion 同步失败: {e}")

    return resource
