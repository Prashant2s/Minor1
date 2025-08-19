# Backend service
FROM python:3.11-slim AS backend

# Install system deps (tesseract for OCR)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app

ENV PYTHONUNBUFFERED=1 \
    UPLOAD_DIR=/data/uploads

# Create uploads dir
RUN mkdir -p /data/uploads
VOLUME ["/data/uploads"]

EXPOSE 5000
CMD ["python", "-m", "app.main"]

