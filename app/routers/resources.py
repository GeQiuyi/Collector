from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resource
from app.schemas import ResourceOut, ResourceList, UpdateTagsRequest

router = APIRouter()


@router.get("/resources", response_model=ResourceList)
def list_resources(
    search: str | None = Query(None, description="搜索标题和摘要"),
    source: str | None = Query(None, description="按来源筛选"),
    tag: str | None = Query(None, description="按标签筛选"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Resource)

    if search:
        like = f"%{search}%"
        query = query.filter(
            Resource.title.ilike(like) | Resource.summary.ilike(like)
        )

    if source:
        query = query.filter(Resource.source == source)

    if tag:
        like_tag = f"%{tag}%"
        query = query.filter(Resource.tags.ilike(like_tag))

    total = query.with_entities(func.count(Resource.id)).scalar()
    items = (
        query.order_by(Resource.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return ResourceList(items=items, total=total, page=page, size=size)


@router.patch("/resources/{resource_id}/tags", response_model=ResourceOut)
def update_tags(
    resource_id: int, req: UpdateTagsRequest, db: Session = Depends(get_db)
):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource.tags = ",".join(t.strip() for t in req.tags if t.strip())
    db.commit()
    db.refresh(resource)
    return resource


@router.get("/tags", response_model=list[str])
def list_tags(db: Session = Depends(get_db)):
    rows = db.query(Resource.tags).filter(Resource.tags != "").all()
    tag_set: set[str] = set()
    for (tags_str,) in rows:
        for t in tags_str.split(","):
            t = t.strip()
            if t:
                tag_set.add(t)
    return sorted(tag_set)


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(resource)
    db.commit()
    return {"ok": True}
