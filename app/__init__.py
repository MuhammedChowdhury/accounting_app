import os
import logging
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import pymysql

pymysql.install_as_MySQLdb()

# ✅ Initialize Extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

    # ✅ Database Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, '..', 'instance')
    os.makedirs(instance_dir, exist_ok=True)

    default_sqlite_path = f"sqlite:///{os.path.abspath(os.path.join(instance_dir, 'app.db'))}"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", default_sqlite_path)


    # ✅ Initialize Flask Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth_routes.login"

    # ✅ Define User Model
    from app.models import User as DBUser

    @login_manager.user_loader
    def load_user(user_id):
        return DBUser.query.get(int(user_id))

    # ✅ Register Blueprints (No Duplicate Imports)
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
    from app.routes.transaction_routes import transaction_routes
    from app.routes.auth_routes import auth_routes
    from app.routes.subscribe_routes import subscribe_routes

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
    app.register_blueprint(transaction_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(subscribe_routes)

    # ✅ Root Route (Restricted)
    @app.route('/index')
    @login_required
    def home():
        routes = [rule.rule for rule in app.url_map.iter_rules() if "static" not in rule.rule]
        return render_template("index.html", routes=routes)

   

     # ✅ Logout Route
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("auth_routes.login"))

    # ✅ Landing Route (for all users)
    @app.route("/")
    def index():
        return render_template("welcome.html")
   
      

    print("\n🔍 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule.endpoint, "→", rule.rule)

    return app