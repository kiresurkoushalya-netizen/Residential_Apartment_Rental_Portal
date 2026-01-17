from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from extensions import db
from config import Config

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.booking_api import booking_bp
from routes.tower_api import tower_bp
from routes.unit_api import unit_bp
from routes.amenity_api import amenity_bp
from routes.tenant_api import tenant_bp
from routes.dashboard_api import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ CORS FIX (Angular + JWT Authorization Header + OPTIONS preflight)
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:4200"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # ✅ FIX: Always return 200 OK for OPTIONS preflight
    @app.before_request
    def handle_options_preflight():
        if request.method == "OPTIONS":
            return "", 200

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # ✅ Booking API under /api
    app.register_blueprint(booking_bp, url_prefix="/api")

    app.register_blueprint(tower_bp, url_prefix="/api/tower")
    app.register_blueprint(unit_bp, url_prefix="/api/")
    app.register_blueprint(amenity_bp, url_prefix="/api/amenity")
    app.register_blueprint(tenant_bp, url_prefix="/api/tenant")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashbard")

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
