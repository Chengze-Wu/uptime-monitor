from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import config
import os
from app.extensions import db, migrate


def create_app():
    app = Flask(__name__)

    # Initial configs
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[env])

    # Initial app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    with app.app_context():
        from app.models import (
            Organization, Team, User, Monitor,
            CheckResult, SSLCertificate, NotificationRule,
            MaintenanceWindow, Incident, Report
        )

        from app.routes.auth import auth_bp
        from app.routes.users import users_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(users_bp)

    # Register error handler
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def server_error(e):
        return {'error': 'Internal server error'}, 500

    # health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    return app