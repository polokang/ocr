from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import List, Literal
from easyocrapi import EasyOCRAPI
from tesseractapi import TesseractAPI
from azureocrapi import AzureOCRAPI

# 配置更详细的日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# 初始化OCR引擎
easy_ocr = EasyOCRAPI()
tesseract_ocr = TesseractAPI()
azure_ocr = AzureOCRAPI()

class ImageRequest(BaseModel):
    image_path: str
    type: Literal["easyocr", "tesseract", "azure"] = "easyocr"
    language: str = "en"  # 默认使用英文模式

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
        
        # 根据type参数选择OCR引擎
        if request.type == "easyocr":
            extracted_text = easy_ocr.extract_text(request.image_path)
        elif request.type == "tesseract":
            extracted_text = tesseract_ocr.extract_text(request.image_path)
        else:
            extracted_text = azure_ocr.extract_text(request.image_path, language=request.language)
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 