import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # ✅ Secure Flask Sessions
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

    # ✅ Define Custom Template Directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.template_folder = template_dir

    # ✅ Configure Database
    db_path = os.path.abspath('instance/app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Set Up Logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info(f"Resolved Database Path: {db_path}")

    # ✅ Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Enforce Foreign Keys in SQLite
    with app.app_context():
        from sqlalchemy import event
        @event.listens_for(db.engine, "connect")
        def enable_foreign_keys(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()

    # ✅ Register Blueprints (Routes)
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

    app.register_blueprint(transaction_routes, url_prefix='/transactions')
    app.register_blueprint(financial_routes, url_prefix='/financial')
    app.register_blueprint(bas_routes, url_prefix='/bas')
    app.register_blueprint(company_routes, url_prefix='/company')
    app.register_blueprint(payroll_routes, url_prefix='/payroll')
    app.register_blueprint(cash_flow_routes, url_prefix='/cashflow')
    app.register_blueprint(ledger_routes, url_prefix='/ledger')
    app.register_blueprint(quote_routes, url_prefix='/quotes')
    app.register_blueprint(invoice_routes, url_prefix='/invoices')
    app.register_blueprint(purchase_order_routes, url_prefix='/purchase-orders')
    app.register_blueprint(bill_routes, url_prefix='/bills')

    # ✅ Root Route
    @app.route('/')
    def home():
        return {"message": "Welcome to the Financial Management Application!"}

    return app
