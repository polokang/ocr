from fastapi import APIRouter, UploadFile, File, HTTPException
from ...services import AzureOCRAPI, EasyOCRAPI, TesseractAPI
from ...db.mongodb import db
from ...core.config import settings
import os
import aiofiles
from datetime import datetime

router = APIRouter()

# 初始化OCR服务
azure_ocr = AzureOCRAPI()
easy_ocr = EasyOCRAPI()
tesseract_ocr = TesseractAPI()

@router.post("/upload-and-ocr/")
async def upload_and_ocr(
    file: UploadFile = File(...),
    engine: str = "easyocr",
    language: str = "en"
):
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "只支持图片文件")
    
    # 保存文件
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # 执行OCR
    try:
        if engine == "azure":
            text = azure_ocr.extract_text(file_path, language)
        elif engine == "tesseract":
            text = tesseract_ocr.extract_text(file_path)
        else:
            text = easy_ocr.extract_text(file_path)
            
        # 保存到MongoDB
        image_doc = {
            "filename": filename,
            "file_path": file_path,
            "upload_time": datetime.utcnow(),
            "ocr_results": text,
            "ocr_engine": engine
        }
        
        await db.db.images.insert_one(image_doc)
        
        return {
            "status": "success",
            "filename": filename,
            "text": text
        }
        
    except Exception as e:
        raise HTTPException(500, f"OCR处理失败: {str(e)}") 