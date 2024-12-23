from fastapi import FastAPI, HTTPException
import easyocr
from pydantic import BaseModel
import logging
import os
from typing import List

# 配置更详细的日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

try:
    # 初始化 EasyOCR reader（支持中英文）
    logger.info("正在初始化 EasyOCR...")
    reader = easyocr.Reader(['ch_sim', 'en'])
    logger.info("EasyOCR 初始化成功")
except Exception as e:
    logger.error(f"EasyOCR 初始化失败: {str(e)}")
    raise

class ImageRequest(BaseModel):
    image_path: str

class OCRResponse(BaseModel):
    status: str
    text: List[str]
    error: str = None

@app.post("/ocr/", response_model=OCRResponse)
async def extract_text(request: ImageRequest):
    try:
        logger.debug(f"接收到图片路径: {request.image_path}")
        
        # 检查文件是否存在
        if not os.path.exists(request.image_path):
            logger.error(f"文件不存在: {request.image_path}")
            raise HTTPException(status_code=404, detail="图片文件不存在")
        
        # 检查文件大小
        file_size = os.path.getsize(request.image_path)
        logger.debug(f"文件大小: {file_size} bytes")
        
        # 检查文件扩展名
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        file_ext = os.path.splitext(request.image_path)[1].lower()
        if file_ext not in valid_extensions:
            raise HTTPException(status_code=400, detail="不支持的图片格式")
        
        # 读取图片并识别文字
        logger.debug("开始识别文字...")
        result = reader.readtext(request.image_path)
        
        # 提取识别到的文字
        extracted_text = []
        for detection in result:
            text = detection[1]
            extracted_text.append(text)
        
        logger.debug(f"识别结果: {extracted_text}")
        return OCRResponse(
            status="success",
            text=extracted_text
        )
    except HTTPException as he:
        logger.error(f"HTTP错误: {str(he)}")
        raise
    except Exception as e:
        logger.error(f"发生错误: {str(e)}", exc_info=True)
        return OCRResponse(
            status="error",
            text=[],
            error=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 