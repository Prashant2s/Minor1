from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import logging
import os
from datetime import datetime

from ..services.images import save_and_process_file, is_allowed_file
from ..services.ocr import run_ocr
from ..services.extract import generate_certificate_summary
from ..core.config import settings

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)

def add_cors(response):
    """Add CORS headers."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@api_bp.route("/summarize", methods=['POST', 'OPTIONS'])
def summarize_document():
    """Simple document summarization endpoint."""
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
        upload_path.mkdir(parents=True, exist_ok=True)
        file_path = upload_path / filename
        
        # Process file and extract text
        processed_path, file_type = save_and_process_file(file.stream, file_path)
        ocr_text = run_ocr(processed_path)
        
        if not ocr_text.strip():
            response = jsonify({"error": "No text could be extracted from the document"})
            response.status_code = 400
            return add_cors(response)
        
        # Generate summary using AI
        summary = generate_certificate_summary(ocr_text, {})
        
        response = jsonify({
            "file_type": file_type,
            "summary": summary,
            "extracted_text_length": len(ocr_text),
            "processed_at": datetime.now().isoformat()
        })
        response.status_code = 200
        return add_cors(response)
        
    except Exception as e:
        logger.error(f"Document summarization failed: {str(e)}")
        response = jsonify({"error": f"Processing failed: {str(e)}"})
        response.status_code = 500
        return add_cors(response)

@api_bp.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "document-summarizer"})