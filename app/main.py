import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

from sqlalchemy import inspect, text
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app.routers import collect, resources

Base.metadata.create_all(bind=engine)

with engine.connect() as conn:
    columns = [c["name"] for c in inspect(engine).get_columns("resources")]
    if "tags" not in columns:
        conn.execute(text("ALTER TABLE resources ADD COLUMN tags TEXT DEFAULT ''"))
        conn.commit()

app = FastAPI(title="Collector", description="跨平台稍后读收集器")

app.include_router(collect.router, prefix="/api")
app.include_router(resources.router, prefix="/api")
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
