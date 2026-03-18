from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resource
from app.schemas import CollectRequest, ResourceOut
from app.parser import parse

router = APIRouter()


@router.post("/collect", response_model=ResourceOut)
def collect(req: CollectRequest, db: Session = Depends(get_db)):
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
    return resource
