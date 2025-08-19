# University Verifier

A Docker-first React + Flask + PostgreSQL application with OCR and optional AI extraction.

Quick start
- Copy .env.example to .env and set POSTGRES_PASSWORD (no quotes).
- Build and run:
  - docker compose --env-file .env up --build
- App URLs:
  - Frontend: http://localhost:5173
  - Backend: http://localhost:5000/health

Frontend
- Vite + React + TS + MUI + Axios
- Configure API URL with env VITE_API_URL (compose sets it).

Backend
- Flask with SQLAlchemy and Alembic-ready structure
- OCR via Tesseract (pytesseract)
- Upload dir mounted at /data/uploads

API
- POST /api/v1/certificates/upload (multipart/form-data, field name: file)
- GET /api/v1/certificates
- GET /api/v1/certificates/{id}

Notes
- For AI extraction later, set OPENAI_API_KEY in the backend environment and extend services/extract.py.
- For EasyOCR switch, update services/ocr.py to use EasyOCR Reader.

