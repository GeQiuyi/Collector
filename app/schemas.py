from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator


class CollectRequest(BaseModel):
    content: str
    tags: list[str] = []


class UpdateTagsRequest(BaseModel):
    tags: list[str]


class ResourceOut(BaseModel):
    id: int
    title: str | None
    url: str | None
    source: str
    summary: str | None
    tags: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        return v


class ResourceList(BaseModel):
    items: list[ResourceOut]
    total: int
    page: int
    size: int
