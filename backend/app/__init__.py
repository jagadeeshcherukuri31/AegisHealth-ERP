from flask import Flask, jsonify
from .config import Config
from .extensions import cors, db, jwt


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from . import models  # noqa: F401  (register models)
    from .routes import auth, patients, appointments, ehr, billing, pharmacy, dashboard
    for m in (auth, patients, appointments, ehr, billing, pharmacy, dashboard):
        app.register_blueprint(m.bp)

    @app.errorhandler(404)
    def nf(_):
        return jsonify(error="Not found"), 404

    @app.errorhandler(ValueError)
    def bad(e):
        return jsonify(error=str(e)), 400

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    return app
