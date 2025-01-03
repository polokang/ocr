from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "OCR Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB设置
    MONGODB_URL: str = "mongodb+srv://aqureporter:ssPVpwiQNw3bBi6m@cluster0.yvch9d8.mongodb.net/"
    MONGODB_DB: str = "ocr_service"
    
    # Azure设置
    AZURE_KEY: str = "5BcnQclzVumA5wfS4kyw8gkzt6JqNGMglUizrxnkMVT2SQ5atSfxJQQJ99BAACL93NaXJ3w3AAAFACOGX97g"
    AZURE_ENDPOINT: str = "https://hunter-ocr.cognitiveservices.azure.com/"
    
    # 文件上传设置
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"

settings = Settings() 