import pytesseract
from PIL import Image
import logging
import os
from typing import List

logger = logging.getLogger(__name__)

class TesseractAPI:
    def __init__(self):
        try:
            # Windows 系统下配置 Tesseract 路径
            if os.name == 'nt':  # Windows 系统
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            logger.info("Tesseract API 初始化成功")
        except Exception as e:
            logger.error(f"Tesseract API 初始化失败: {str(e)}")
            raise

    def extract_text(self, image_path: str) -> List[str]:
        try:
            logger.debug("开始使用Tesseract识别文字...")
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            # 将文本按行分割并过滤空行
            result = [line.strip() for line in text.split('\n') if line.strip()]
            
            logger.debug(f"Tesseract识别结果: {result}")
            return result
        except Exception as e:
            logger.error(f"Tesseract识别失败: {str(e)}")
            raise 