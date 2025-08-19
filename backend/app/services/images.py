from pathlib import Path
from PIL import Image

def save_image(stream, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, 'wb') as f:
        f.write(stream.read())
    # Basic open to ensure it's an image and normalize format
    try:
        img = Image.open(dest)
        img.verify()
    except Exception:
        dest.unlink(missing_ok=True)
        raise ValueError("Invalid image file")
    return dest

