import os
from flask import Flask
from flask_cors import CORS
from app.extensions import db, bcrypt, migrate


def create_app():
    app = Flask(__name__)

    # ---------- Configuration ----------
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-dev-key-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI',
        'mysql+mysqlconnector://root:Hemant%404004@localhost/predict_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Session config (server-side, cookie-based)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

    # ---------- Extensions ----------
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # CORS — allow any localhost port in development
    CORS(app, supports_credentials=True, origins=[
        r'http://localhost:\d+',
        r'http://127\.0\.0\.1:\d+',
    ])

    # ---------- Blueprints ----------
    from app.routes.auth import auth_bp
    from app.routes.customers import customers_bp
    from app.routes.predictions import predictions_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(predictions_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # ---------- Create tables + seed ----------
    with app.app_context():
        from app.models import user, customer, prediction, subscription, usage  # noqa
        db.create_all()
        _seed_plans(app)

    return app


def _seed_plans(app):
    """Seed default subscription plans if they don't exist."""
    from app.models.subscription import SubscriptionPlan
    if SubscriptionPlan.query.count() == 0:
        plans = [
            SubscriptionPlan(
                name='Free', price=0,
                max_customers=50, max_predictions=100,
                features='Basic dashboard,Up to 50 customers,100 predictions/month'
            ),
            SubscriptionPlan(
                name='Pro', price=29,
                max_customers=500, max_predictions=2000,
                features='Advanced analytics,CSV upload,500 customers,2000 predictions/month,Priority support'
            ),
            SubscriptionPlan(
                name='Enterprise', price=99,
                max_customers=10000, max_predictions=50000,
                features='Unlimited analytics,API access,10000 customers,50000 predictions/month,Dedicated support,Custom integrations'
            ),
        ]
        db.session.add_all(plans)
        db.session.commit()
