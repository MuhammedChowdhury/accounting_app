import logging
import os
import secrets
from flask import Flask, request, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions globally
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    """Application Factory core production configuration layer."""
    app = Flask(__name__)

    # 🔒 SECURITY CONTROL: Pull secret key from production environment or auto-generate
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    
    # 🔒 DATABASE CONTROL: Check for live cloud database (PostgreSQL/MySQL), or fallback to local SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///accounting.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with current application context
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth_routes.login"

    # Force Python to load ALL models into memory immediately
    from app.models import (
        User,
        Company,
        Subscriber,
        FinancialRecord,
        PayrollRecord,
        AssetLiability,
        Equity,
        Quote,
        Invoice,
        PurchaseOrder,
        Bill,
        Sale,
        Employee,
        PayrollRun,
    )

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprint controllers
    from app.routes.auth_routes import auth_routes
    from app.routes.bas_routes import bas_routes
    from app.routes.bill_routes import bill_routes
    from app.routes.cash_flow_routes import cash_flow_routes
    from app.routes.company_routes import company_routes
    from app.routes.financial_routes import financial_routes
    from app.routes.invoice_routes import invoice_routes
    from app.routes.ledger_routes import ledger_routes
    from app.routes.payroll_routes import payroll_routes
    from app.routes.purchase_order_routes import purchase_order_routes
    from app.routes.quote_routes import quote_routes
    from app.routes.report_routes import report_routes
    from app.routes.subscribe_routes import subscribe_routes
    from app.routes.transaction_routes import transaction_routes

    app.register_blueprint(auth_routes)
    app.register_blueprint(bas_routes)
    app.register_blueprint(bill_routes)
    app.register_blueprint(cash_flow_routes)
    app.register_blueprint(company_routes)
    app.register_blueprint(financial_routes)
    app.register_blueprint(invoice_routes)
    app.register_blueprint(ledger_routes)
    app.register_blueprint(payroll_routes)
    app.register_blueprint(purchase_order_routes)
    app.register_blueprint(quote_routes)
    app.register_blueprint(report_routes)
    app.register_blueprint(subscribe_routes)
    app.register_blueprint(transaction_routes)

    # Makes company and companies available in every template
    @app.context_processor
    def inject_active_company():
        company_id = session.get("company_id") or request.args.get("company_id", type=int)

        try:
            companies = db.session.query(Company).all()
        except Exception:
            companies = []

        if company_id:
            try:
                company = db.session.get(Company, int(company_id))
                if company:
                    return dict(company=company, companies=companies)
            except Exception:
                pass

        return dict(company=None, companies=companies)

    # Homepage Matrix Navigation Gate
    @app.route("/")
    @app.route("/index")
    def index():
        company_id = session.get("company_id") or request.args.get("company_id", type=int)
        if not company_id:
            return redirect(url_for('company_routes.select_company'))
        return render_template("welcome.html")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
