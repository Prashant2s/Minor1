### Quick start (Docker, recommended)
- **Prerequisites**: Install Docker Desktop.
- **Clone the repo**:
```bash
git clone https://github.com/your-org/university-verifier.git
cd university-verifier
```
- **Create `.env` in the project root**:
```env
POSTGRES_PASSWORD=app
```
- **Start everything**:
```bash
docker compose up -d --build
```
- **Open the app**:
  - Frontend: http://localhost:5173
  - Backend health: http://localhost:5000/health (should return {"status":"ok"})

- **Stop**:
```bash
docker compose down
```
- **Reset DB (wipe data) if passwords change or you want a clean start**:
```bash
docker compose down -v
```

### Common Docker commands
- **See service status**:
```bash
docker compose ps
```
- **Follow logs**:
```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### Optional: run locally without Docker
Only if you prefer a local setup. Otherwise, skip this.

- **Prerequisites**
  - Python 3.11
  - Node.js 20
  - Tesseract OCR
    - Windows: install Tesseract (UB Mannheim build is fine), add to PATH
    - macOS: `brew install tesseract`
    - Ubuntu/Debian: `sudo apt-get install -y tesseract-ocr libgl1`

- **Start Postgres (easiest with Docker)**:
```bash
docker run --name uv-db -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app -e POSTGRES_DB=university -p 5432:5432 -d postgres:16
```

- **Backend**
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Env vars
$env:DB_URL="postgresql+psycopg2://app:app@localhost:5432/university"   # PowerShell
export DB_URL="postgresql+psycopg2://app:app@localhost:5432/university"  # macOS/Linux
$env:CORS_ORIGIN="http://localhost:5173"
$env:UPLOAD_DIR="$(Resolve-Path ..)/uploads"  # or any absolute path
python -m app.main
# Backend runs at http://localhost:5000
```

- **Frontend**
```bash
cd frontend
npm ci
# Make sure API points to backend:
# Vite uses VITE_API_URL at build/runtime; docker sets it automatically.
# For local dev, create .env.local with:
#   VITE_API_URL=http://localhost:5000/api/v1
npm run dev
# Open http://localhost:5173
```

### Troubleshooting
- **Backend can’t connect to DB (password auth failed)**: Ensure `.env` `POSTGRES_PASSWORD` matches; if you changed it, run `docker compose down -v` then `docker compose up -d --build`.
- **Port already in use (5000 or 5173)**: Stop conflicting apps or edit `docker-compose.yml` port mappings.
- **Tesseract not found (non-Docker run)**: Install Tesseract and ensure it’s on PATH.
- **CORS issues (non-Docker run)**: Set `CORS_ORIGIN` to your frontend origin (e.g., `http://localhost:5173`).

- The easiest path for your friend is Docker: create `.env` with `POSTGRES_PASSWORD=app`, run `docker compose up -d --build`, then visit http://localhost:5173.




University Verifier

A Docker-first React + Flask + PostgreSQL application with OCR and optional AI extraction.
run this-
docker compose up -d
docker compose ps --all
You can now access:
•  Frontend: http://localhost:5173
•  Backend: http://localhost:5000/health
•  API base: http://localhost:5000/api/v1

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
