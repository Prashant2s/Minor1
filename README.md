University Verifier

A Docker-first React + Flask + PostgreSQL application with OCR and optional AI extraction.

Quick start
•  Copy .env.example to .env and set POSTGRES_PASSWORD (no quotes).
•  Build and run:
•  docker compose --env-file .
Stopped task 4/5: "Export secure POSTGRES_PASSWORD for this session"
~\university-verifier
give me the README.md with how to run the project
University Verifier

A Docker-first web app for verifying university certificates:
•  Frontend: React + TypeScript + Vite + Material-UI + Axios
•  Backend: Python + Flask + SQLAlchemy
•  Database: PostgreSQL
•  OCR: Tesseract (via pytesseract), swap to EasyOCR later if desired
•  Containerized with Docker and Docker Compose

Features

•  Upload certificate images
•  OCR text extraction
•  Naive field extraction (name, registration number, degree, etc.)
•  Browse records and view details with the original image

Project structure

•  backend/
•  app/
◦  api/routes.py
◦  core/config.py
◦  db/{models.py, session.py}
◦  services/{ocr.py, images.py, extract.py}
◦  main.py
•  requirements.txt
•  frontend/
•  src/{pages, api, assets, App.tsx, main.tsx}
•  package.json, vite config, tsconfigs
•  docker/
•  backend.Dockerfile
•  frontend.Dockerfile
•  docker-compose.yml
•  .env.example (copy to .env)
•  .gitignore

Prerequisites

•  Docker Desktop (Windows/macOS) or Docker Engine
•  PowerShell on Windows (commands below use pwsh syntax)

Quick start (Docker-first)

1) Copy and configure environment
•  PowerShell, in the project root:
•  Copy-Item .env.example .env
•  Open .env and set POSTGRES_PASSWORD to a real value (no quotes).
•  Optional: set OPENAI_API_KEY if you plan to integrate AI extraction later.

2) Build and start services
•  docker compose --env-file .env up --build -d

3) Verify services
•  Backend health:
•  Invoke-WebRequest -UseBasicParsing http://localhost:5000/health | Select-Object -ExpandProperty Content
•  Expected: {"status":"ok"}
•  Frontend:
•  Open http://localhost:5173 in your browser

4) Use the app
•  Upload a certificate image on the frontend (or via API below)
•  View records and details pages

5) Stop services
•  Keep volumes/data:
•  docker compose down
•  Remove volumes/data (reset DB):
•  docker compose down -v

Environment variables

•  POSTGRES_PASSWORD (required): password for DB user app
•  OPENAI_API_KEY (optional): for future AI-based extraction
•  The compose file supplies:
•  DB_URL to backend
•  UPLOAD_DIR to backend (/data/uploads)
•  VITE_API_URL to frontend (http://localhost:5000/api/v1)

API

Base URL: http://localhost:5000/api/v1

•  POST /certificates/upload
•  multipart/form-data, field name: file (image/*)
•  GET /certificates
•  GET /certificates/{id}
•  GET /certificates/{id}/image

Example upload (PowerShell):
•  $form = @{ file = Get-Item 'C:\path\to\certificate.jpg' }
•  Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://localhost:5000/api/v1/certificates/upload -Form $form

Local development (optional, without Docker)

Backend
•  py -3 -m venv .venv
•  ..venv\Scripts\Activate.ps1
•  pip install -r backend\requirements.txt
•  Ensure Postgres is running (you can still use docker compose up db)
•  Set environment variables:
•  $env:DB_URL = "postgresql+psycopg2://app:YOUR_PASSWORD@localhost:5432/university"
•  $env:CORS_ORIGIN = "http://localhost:5173"
•  $env:UPLOAD_DIR = "$PWD\data\uploads"
•  Run:
•  Push-Location backend
•  python -m app.main
•  Pop-Location
•  Health: http://localhost:5000/health

Frontend
•  Push-Location frontend
•  npm ci
•  npm run dev (or npm run preview after npm run build)
•  Pop-Location
•  App: http://localhost:5173

Troubleshooting

•  Backend container exits with “password authentication failed for user 'app'”
•  Ensure POSTGRES_PASSWORD is set in .env and matches the compose environment
•  Recreate stack with a clean DB:
◦  docker compose down -v
◦  docker compose --env-file .env up --build -d
•  Tesseract/OCR issues
•  The backend image installs tesseract-ocr. If OCR quality is poor, consider preprocessing (backend/app/services/images.py) or switching to EasyOCR (edit backend/app/services/ocr.py).
•  CORS or API URL issues
•  Frontend uses VITE_API_URL from compose. If running components separately, ensure VITE_API_URL points to http://localhost:5000/api/v1.

Security

•  Do not commit .env. The repository includes .env.example for reference.
•  Use strong POSTGRES_PASSWORD values.

License

MIT (or your preferred license).
