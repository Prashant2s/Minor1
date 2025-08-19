from typing import List
import os

class Settings:
    def __init__(self) -> None:
        self.DB_URL: str = os.getenv("DB_URL", "postgresql+psycopg2://app:app@db:5432/university")
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
        self.OCR_ENGINE: str = os.getenv("OCR_ENGINE", "tesseract")  # easyocr|tesseract
        self.CORS_ORIGINS: List[str] = [os.getenv("CORS_ORIGIN", "*")]
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/data/uploads")

settings = Settings()
