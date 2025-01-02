from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "OCR Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB设置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "ocr_service"
    
    # Azure设置
    AZURE_KEY: str = "your_key"
    AZURE_ENDPOINT: str = "https://hunter-ocr.cognitiveservices.azure.com/"
    
    # 文件上传设置
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"

settings = Settings() 