from pathlib import Path
import pytesseract
from PIL import Image
from ..core.config import settings


def run_ocr(image_path: Path) -> str:
    # For simplicity, use Tesseract by default. EasyOCR can be plugged similarly.
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

