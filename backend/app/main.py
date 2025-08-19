from flask import Flask
from flask_cors import CORS
from .db.session import init_engine, db_session, Base, get_engine
from .api.routes import api_bp
from .core.config import settings


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": settings.CORS_ORIGINS}})

    # DB
    init_engine(settings.DB_URL)

    # Ensure models are imported and tables are created on startup (simple dev path)
    from .db import models  # noqa: F401
    Base.metadata.create_all(bind=get_engine())

    @app.teardown_appcontext
    def remove_session(exception=None):
        db_session.remove()

    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

