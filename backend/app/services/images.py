from pathlib import Path
from PIL import Image

def save_and_process_file(stream, dest: Path):
    """Save uploaded file and return processed path and file type."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the file
    with open(dest, 'wb') as f:
        f.write(stream.read())
    
    # Determine file type and process if needed
    file_extension = dest.suffix.lower()
    
    if file_extension in ['.jpg', '.jpeg', '.png', '.tiff', '.tif']:
        # It's an image file
        try:
            img = Image.open(dest)
            img.verify()  # Verify it's a valid image
            return dest, 'image'
        except Exception:
            dest.unlink(missing_ok=True)
            raise ValueError("Invalid image file")
    
    elif file_extension == '.pdf':
        # For PDF, we'll need to convert to image first
        # For now, return as PDF type - you might want to add PDF processing
        return dest, 'pdf'
    
    else:
        dest.unlink(missing_ok=True)
        raise ValueError(f"Unsupported file type: {file_extension}")

def is_allowed_file(filename: str) -> bool:
    """Check if file type is allowed."""
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif'}
    return Path(filename).suffix.lower() in allowed_extensions

