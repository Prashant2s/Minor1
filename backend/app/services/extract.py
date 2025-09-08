from ..core.config import settings
import openai
import logging

logger = logging.getLogger(__name__)

def generate_certificate_summary(ocr_text: str, extracted_fields: dict) -> str:
    """Generate a summary of the document using DeepSeek AI if available."""
    if settings.DEEPSEEK_API_KEY:
        try:
            client = openai.OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Summarize this document text in 2-3 sentences. Focus on the key information like student name, degree, institution, and any important details."},
                    {"role": "user", "content": ocr_text}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"DeepSeek summary failed: {e}")
            return generate_simple_summary(ocr_text)
    else:
        return generate_simple_summary(ocr_text)

def generate_simple_summary(ocr_text: str) -> str:
    """Generate a simple summary without AI."""
    lines = [l.strip() for l in ocr_text.splitlines() if l.strip()]
    if len(lines) > 0:
        return f"Document contains {len(lines)} lines of text. First line: {lines[0][:100]}..."
    return "No text content found in document."

