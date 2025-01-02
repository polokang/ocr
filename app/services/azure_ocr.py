from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import logging
from typing import List
from ..core.config import settings

logger = logging.getLogger(__name__)

class AzureOCRAPI:
    def __init__(self):
        try:
            subscription_key = settings.AZURE_KEY
            endpoint = settings.AZURE_ENDPOINT

            self.client = ComputerVisionClient(
                endpoint=endpoint,
                credentials=CognitiveServicesCredentials(subscription_key)
            )
            logger.info("Azure OCR API 初始化成功")
        except Exception as e:
            logger.error(f"Azure OCR API 初始化失败: {str(e)}")
            raise

    def extract_text(self, image_path: str, language: str = "en") -> List[str]:
        try:
            logger.debug(f"开始使用Azure OCR识别文字，语言模式：{language}...")
            
            with open(image_path, "rb") as image_file:
                result = self.client.recognize_printed_text_in_stream(
                    image=image_file,
                    language=language,
                    detect_orientation=True
                )

                extracted_text = []
                if result:
                    for region in result.regions:
                        for line in region.lines:
                            line_text = ""
                            for word in line.words:
                                line_text += word.text + " "
                            extracted_text.append(line_text.strip())

            logger.debug(f"Azure OCR识别结果: {extracted_text}")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Azure OCR识别失败: {str(e)}", exc_info=True)
            raise 