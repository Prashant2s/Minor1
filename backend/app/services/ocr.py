from pathlib import Path
import pytesseract
from PIL import Image
from ..core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

def run_ocr(image_path: Path) -> str:
    """Extract text from image using Tesseract OCR."""
    try:
        # Set Tesseract path for Windows if not in PATH
        if os.name == 'nt':  # Windows
            tesseract_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
            ]
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
        
        # Try to run OCR
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        if "tesseract" in str(e).lower() and "not found" in str(e).lower():
            raise ValueError(
                "Tesseract OCR is not installed. Please install Tesseract OCR:\n"
                "Windows: winget install UB-Mannheim.TesseractOCR\n"
                "Or download from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                "Make sure to add it to your PATH environment variable."
            )
        else:
            raise ValueError(f"OCR processing failed: {str(e)}")

