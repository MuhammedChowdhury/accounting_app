import os
import logging
from flask import Flask

# Initialize Extensions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # ✅ Ensure 'os' is properly imported
    app = Flask(__name__)

    # ✅ Secret Key to Fix Flash & Sessions
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

    # Define custom template directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.template_folder = template_dir

    # Database Configuration
    db_path = os.path.abspath('instance/app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Logging Configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info(f"Resolved Database Path: {db_path}")

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

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

    # ✅ Fixed Blueprint Registration
    from .routes.quote_routes import quote_routes
    from .routes.invoice_routes import invoice_routes
    from .routes.purchase_order_routes import purchase_order_routes
    from .routes.bill_routes import bill_routes

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

    # Root Route
    @app.route('/')
    def home():
        return {"message": "Welcome to the Financial Management Application!"}

    return app
