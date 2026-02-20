import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from backend.extensions import db, migrate, jwt, limiter, celery
from backend.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure DB is set
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL is not set in .env")

    # ----------------------------
    # Initialize Extensions
    # ----------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    # ----------------------------
    # CORS
    # ----------------------------
    # Inside create_app():
    CORS(
        app,
        supports_credentials=True, # Required for cookies
        origins=["http://localhost:3000"],
        allow_headers=["Content-Type", "Authorization"]
    )

    # ----------------------------
    # Celery Configuration
    # ----------------------------
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # ----------------------------
    # Import Models
    # ----------------------------
    from backend.models.user import User
    from backend.models.lead import Lead
    from backend.models.payment import Payment

    # ----------------------------
    # Register Blueprints
    # ----------------------------
    from backend.routes.leads import leads_bp
    from backend.routes.auth_routes import auth_bp
    from backend.routes.payments import payments_bp
    from backend.routes.chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(leads_bp, url_prefix="/api/leads")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")


    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False             # Disable for testing if needed

    # ----------------------------
    # Health Check
    # ----------------------------
    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200

    # ----------------------------
    # Task Status
    # ----------------------------
    @app.route("/api/tasks/<task_id>")
    def get_task_status(task_id):
        task = celery.AsyncResult(task_id)
        return jsonify({
            "status": task.state,
            "result": str(task.info)
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
