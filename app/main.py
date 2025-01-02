from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.endpoints import ocr
from .db.mongodb import db
import os

# 创建必要的目录
os.makedirs("static/uploads", exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
app.include_router(ocr.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    await db.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await db.close_mongo_connection() 