from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
from ..db.session import db_session
from ..db.models import Certificate, ExtractedField
from ..services.images import save_image
from ..services.ocr import run_ocr
from ..services.extract import extract_fields
from ..core.config import settings

api_bp = Blueprint("api", __name__)

@api_bp.post("/certificates/upload")
def upload_certificate():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    image_path = save_image(file.stream, upload_path / filename)

    # OCR and extraction
    ocr_text = run_ocr(image_path)
    fields = extract_fields(ocr_text)

    cert = Certificate(image_path=str(image_path))
    db_session.add(cert)
    db_session.flush()  # get cert.id

    for k, v in fields.items():
        db_session.add(ExtractedField(certificate_id=cert.id, key=k, value=str(v), confidence=None))

    db_session.commit()

    return jsonify({
        "id": cert.id,
        "image_path": cert.image_path,
        "fields": fields
    }), 201

@api_bp.get("/certificates")
def list_certificates():
    certs = db_session.query(Certificate).order_by(Certificate.id.desc()).limit(100).all()
    out = []
    for c in certs:
        out.append({
            "id": c.id,
            "image_path": c.image_path,
            "created_at": c.created_at.isoformat()
        })
    return jsonify(out)

@api_bp.get("/certificates/<int:cert_id>")
def get_certificate(cert_id: int):
    cert = db_session.get(Certificate, cert_id)
    if not cert:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": cert.id,
        "image_path": cert.image_path,
        "created_at": cert.created_at.isoformat(),
        "fields": [{"key": f.key, "value": f.value, "confidence": f.confidence} for f in cert.fields]
    })

@api_bp.get("/certificates/<int:cert_id>/image")
def get_certificate_image(cert_id: int):
    cert = db_session.get(Certificate, cert_id)
    if not cert:
        return jsonify({"error": "Not found"}), 404
    image_path = Path(cert.image_path)
    if not image_path.exists():
        return jsonify({"error": "Image not found"}), 404
    return send_file(image_path, as_attachment=False)

