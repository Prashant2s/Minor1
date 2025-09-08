from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self) -> None:
        self.DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")
        self.OCR_ENGINE: str = os.getenv("OCR_ENGINE", "tesseract")  # easyocr|tesseract
        self.CORS_ORIGINS: List[str] = [os.getenv("CORS_ORIGIN", "*")]
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")

settings = Settings()
