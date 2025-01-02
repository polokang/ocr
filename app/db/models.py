from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ImageModel(BaseModel):
    filename: str
    file_path: str
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    ocr_results: Optional[List[str]] = None
    ocr_engine: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 