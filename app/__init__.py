import os
import logging
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

# Initialize Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

    # ✅ Database Configuration (Fixing SQLAlchemy Error)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Prevent warnings

    # ✅ Define custom template directory
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    app.template_folder = template_dir

    # Initialize Flask Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"  # Redirects users to login if not authenticated

    class User(UserMixin):
        def __init__(self, id):
            self.id = id

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    # Logging Configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info(f"Resolved Database Path: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Enable Foreign Keys within Application Context
    with app.app_context():
        from sqlalchemy import event
        @event.listens_for(db.engine, "connect")
        def enable_foreign_keys(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    # Register Blueprints
    from .routes.transaction_routes import transaction_routes
    from .routes.financial_routes import financial_routes
    from .routes.bas_routes import bas_routes
    from .routes.company_routes import company_routes
    from .routes.payroll_routes import payroll_routes
    from .routes.cash_flow_routes import cash_flow_routes
    from .routes.ledger_routes import ledger_routes
    from .routes.quote_routes import quote_routes
    from .routes.invoice_routes import invoice_routes
    from .routes.purchase_order_routes import purchase_order_routes
    from .routes.bill_routes import bill_routes
    from .routes.auth_routes import auth_routes  # ✅ Added authentication routes

    app.register_blueprint(transaction_routes, url_prefix='/transaction_routes')
    app.register_blueprint(financial_routes, url_prefix='/financial_routes')
    app.register_blueprint(bas_routes, url_prefix='/bas_routes')
    app.register_blueprint(company_routes, url_prefix='/company_routes')
    app.register_blueprint(payroll_routes, url_prefix='/payroll_routes')
    app.register_blueprint(cash_flow_routes, url_prefix='/cash_flow_routes')
    app.register_blueprint(ledger_routes, url_prefix='/ledger_routes')
    app.register_blueprint(quote_routes, url_prefix='/quote_routes')  
    app.register_blueprint(invoice_routes, url_prefix='/invoice_routes')  
    app.register_blueprint(purchase_order_routes, url_prefix='/purchase_order_routes')  
    app.register_blueprint(bill_routes, url_prefix='/bill_routes')  
    app.register_blueprint(auth_routes, url_prefix='/auth_routes')  # ✅ Registered authentication routes

    # Root Route (Restricted)
    @app.route('/')
    @app.route('/index')
    @login_required
    def home():
        return render_template("index.html")

    return app
