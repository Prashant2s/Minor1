from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import logging

from ..db.session import db_session
from ..db.models import Certificate, ExtractedField, Student
from ..services.images import save_and_process_file, is_allowed_file
from ..services.ocr import run_ocr
from ..services.extract import extract_fields_with_ai, generate_certificate_summary
from ..core.config import settings

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)

def add_cors(response):
    """ CORS headers ."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

def simple_university_verification(extracted_fields: dict) -> dict:
    """Simple verification logic directly in routes."""
    verification_result = {
        "student_verified": False,
        "registration_verified": False,
        "confidence_score": 0.0,
        "matched_student": None
    }
    
    try:
        student_name = extracted_fields.get('student_name')
        reg_number = extracted_fields.get('registration_number')
        
        if reg_number:
            student = db_session.query(Student).filter(Student.reg_no == reg_number).first()
            if student:
                verification_result["student_verified"] = True
                verification_result["registration_verified"] = True
                verification_result["confidence_score"] = 0.8
                verification_result["matched_student"] = {
                    "id": student.id,
                    "name": student.name,
                    "reg_no": student.reg_no
                }
        
        return verification_result
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
        return verification_result

@api_bp.route("/certificates/upload", methods=['POST', 'OPTIONS'])
def upload_certificate():
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors(response)
    
    try:
        if 'file' not in request.files:
            response = jsonify({"error": "No file provided"})
            response.status_code = 400
            return add_cors(response)
            
        file = request.files['file']
        if file.filename == '':
            response = jsonify({"error": "No file selected"})
            response.status_code = 400
            return add_cors(response)
            
        if not is_allowed_file(file.filename):
            response = jsonify({"error": "Invalid file type. Allowed: PDF, JPG, PNG, TIFF"})
            response.status_code = 400
            return add_cors(response)

        filename = secure_filename(file.filename)
        upload_path = Path(settings.UPLOAD_DIR)
        file_path = upload_path / filename
        
        processed_path, file_type = save_and_process_file(file.stream, file_path)
        ocr_text = run_ocr(processed_path)
        
        if not ocr_text.strip():
            response = jsonify({"error": "No text could be extracted"})
            response.status_code = 400
            return add_cors(response)
        
        extracted_fields = extract_fields_with_ai(ocr_text)
        summary = generate_certificate_summary(ocr_text, extracted_fields)
        verification = simple_university_verification(extracted_fields)
        
        cert = Certificate(image_path=str(processed_path), status='processed')
        db_session.add(cert)
        db_session.flush()
        
        for key, value in extracted_fields.items():
            if value:
                field = ExtractedField(certificate_id=cert.id, key=key, value=str(value), confidence=verification.get('confidence_score', 0.0))
                db_session.add(field)
        
        summary_field = ExtractedField(certificate_id=cert.id, key='ai_summary', value=summary, confidence=1.0)
        db_session.add(summary_field)
        db_session.commit()
        
        response = jsonify({
            "id": cert.id,
            "file_type": file_type,
            "summary": summary,
            "extracted_fields": extracted_fields,
            "verification": verification,
            "confidence_score": verification.get('confidence_score', 0.0)
        })
        response.status_code = 201
        return add_cors(response)
        
    except Exception as e:
        db_session.rollback()
        logger.error(f"Certificate upload failed: {str(e)}")
        response = jsonify({"error": f"Processing failed: {str(e)}"})
        response.status_code = 500
        return add_cors(response)

@api_bp.route("/certificates", methods=['GET', 'OPTIONS'])
def list_certificates():
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors(response)
    
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        certs = db_session.query(Certificate).order_by(Certificate.created_at.desc()).limit(limit).offset(offset).all()
        
        result = []
        for cert in certs:
            summary_field = next((f for f in cert.fields if f.key == 'ai_summary'), None)
            summary = summary_field.value if summary_field else "No summary available"
            
            result.append({
                "id": cert.id,
                "status": cert.status,
                "created_at": cert.created_at.isoformat(),
                "summary": summary[:200] + "..." if len(summary) > 200 else summary
            })
        
        response = jsonify({"certificates": result, "count": len(result), "limit": limit, "offset": offset})
        return add_cors(response)
        
    except Exception as e:
        logger.error(f"Failed to list certificates: {str(e)}")
        response = jsonify({"error": "Failed to fetch certificates"})
        response.status_code = 500
        return add_cors(response)

@api_bp.route("/certificates/<int:cert_id>", methods=['GET', 'OPTIONS'])
def get_certificate(cert_id: int):
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors(response)
    
    try:
        cert = db_session.get(Certificate, cert_id)
        if not cert:
            response = jsonify({"error": "Certificate not found"})
            response.status_code = 404
            return add_cors(response)
        
        fields = {}
        summary = ""
        
        for field in cert.fields:
            if field.key == 'ai_summary':
                summary = field.value
            else:
                fields[field.key] = {"value": field.value, "confidence": field.confidence}
        
        response = jsonify({
            "id": cert.id,
            "status": cert.status,
            "created_at": cert.created_at.isoformat(),
            "summary": summary,
            "extracted_fields": fields,
            "field_count": len(fields)
        })
        return add_cors(response)
        
    except Exception as e:
        logger.error(f"Failed to get certificate {cert_id}: {str(e)}")
        response = jsonify({"error": "Failed to fetch certificate"})
        response.status_code = 500
        return add_cors(response)

@api_bp.route("/certificates/<int:cert_id>/image", methods=['GET', 'OPTIONS'])
def get_certificate_image(cert_id: int):
    if request.method == 'OPTIONS':
        response = jsonify({})
        return add_cors(response)
    
    try:
        cert = db_session.get(Certificate, cert_id)
        if not cert:
            response = jsonify({"error": "Certificate not found"})
            response.status_code = 404
            return add_cors(response)
            
        image_path = Path(cert.image_path)
        if not image_path.exists():
            response = jsonify({"error": "Image file not found"})
            response.status_code = 404
            return add_cors(response)
            
        return send_file(image_path, as_attachment=False)
        
    except Exception as e:
        logger.error(f"Failed to serve image: {str(e)}")
        response = jsonify({"error": "Failed to serve image"})
        response.status_code = 500
        return add_cors(response)

