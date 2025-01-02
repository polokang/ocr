import easyocr
import logging
from typing import List

logger = logging.getLogger(__name__)

class EasyOCRAPI:
    def __init__(self):
        try:
            logger.info("正在初始化 EasyOCR...")
            self.reader = easyocr.Reader(['ch_sim', 'en'])
            logger.info("EasyOCR 初始化成功")
        except Exception as e:
            logger.error(f"EasyOCR 初始化失败: {str(e)}")
            raise

    def extract_text(self, image_path: str) -> List[str]:
        try:
            logger.debug("开始使用EasyOCR识别文字...")
            result = self.reader.readtext(image_path)
            
            extracted_text = []
            for detection in result:
                text = detection[1]
                extracted_text.append(text)
            
            logger.debug(f"EasyOCR识别结果: {extracted_text}")
            return extracted_text
        except Exception as e:
            logger.error(f"EasyOCR识别失败: {str(e)}")
            raise 