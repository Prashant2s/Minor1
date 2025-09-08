from flask import Flask
from flask_cors import CORS
from .api.routes import api_bp
from .core.config import settings


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": settings.CORS_ORIGINS}})

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

