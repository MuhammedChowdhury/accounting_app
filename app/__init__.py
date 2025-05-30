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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Initialize Flask Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    # ✅ Define User Model
    class User(UserMixin):
        def __init__(self, id):
            self.id = id

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

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

    # ✅ Root Route (Restricted)
    @app.route('/')
    @app.route('/index')
    @login_required
    def home():
        routes = [rule.rule for rule in app.url_map.iter_rules() if "static" not in rule.rule]
        return render_template("index.html", routes=routes)

    # ✅ Login Route
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username == "admin" and password == "password123":
                user = User(id=username)
                login_user(user)
                return redirect(url_for("home"))

            return "Invalid credentials", 401

        return render_template("login.html")

    # ✅ Logout Route
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    return app
