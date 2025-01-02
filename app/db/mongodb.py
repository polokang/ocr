from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_mongo(self):
        logger.info("连接到MongoDB...")
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB]
        logger.info("MongoDB连接成功")

    async def close_mongo_connection(self):
        logger.info("关闭MongoDB连接...")
        if self.client:
            self.client.close()
            logger.info("MongoDB连接已关闭")

db = MongoDB() 