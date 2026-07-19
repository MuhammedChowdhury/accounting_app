from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric, CheckConstraint
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# =========================================================================
# 1. INDEPENDENT BASE SUITE MODELS (No external dependencies)
# =========================================================================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
     #  ADD THIS EXACT LINE TO TRACK THE ACCOUNT TYPE:
    role = db.Column(db.String(50), default='Bookkeeper', nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    validity_period = db.Column(db.Date, nullable=False)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), default='Pending')

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_status = db.Column(db.String(50), default='Pending')

class Bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), default='Unpaid')

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    tfn = db.Column(db.String(20), nullable=True)
    employment_type = db.Column(db.String(50), default="Full-Time")
    tfn_declaration_status = db.Column(db.String(50), default="Submitted")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PayrollRun(db.Model):
    __tablename__ = "payroll_run"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    pay_period_start = db.Column(db.String(50), nullable=False)
    pay_period_end = db.Column(db.String(50), nullable=False)
    gross_wages = db.Column(db.Float, default=0.0, nullable=False)
    payg_withholding = db.Column(db.Float, default=0.0, nullable=False)
    super_guarantee = db.Column(db.Float, default=0.0, nullable=False)
    net_pay = db.Column(db.Float, default=0.0, nullable=False)
    stp_status = db.Column(db.String(50), default="Pending Submission")
    stp_submission_id = db.Column(db.String(100), nullable=True)
    ato_response_timestamp = db.Column(db.DateTime, nullable=True)
    digital_declaration_signed_by = db.Column(db.String(150), nullable=True)

    employee = db.relationship("Employee", backref="payroll_runs")

# =========================================================================
# 2. DEPENDENT ACCOUNTING SUB-CLASSES (Must compile BEFORE Master Company)
# =========================================================================

class FinancialRecord(db.Model):
    __tablename__ = 'financial_records'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    debit = db.Column(db.Float, default=0.0)
    credit = db.Column(db.Float, default=0.0)
    type_of_expense = db.Column(db.String(50), nullable=True)
    type_of_income = db.Column(db.String(50), nullable=True)
    net_expenses = db.Column(db.Float, default=0.0)
    gst_paid = db.Column(db.Float, default=0.0)
    net_income = db.Column(db.Float, default=0.0)
    gst_received = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)
    invoice = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    company = relationship("Company", back_populates="financial_records")

class PayrollRecord(db.Model):
    __tablename__ = 'payroll_records'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    gross_wages = db.Column(db.Float, nullable=False)
    payg_withholding = db.Column(db.Float, default=0.0)
    superannuation = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    net_pay = db.Column(db.Float, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    company = relationship("Company", back_populates="payroll_records")

class AssetLiability(db.Model):
    __tablename__ = 'assets_liabilities'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False, default=0.0)

    __table_args__ = (
        CheckConstraint("category IN ('Asset', 'Liability')", name="ck_asset_liability_category"),
    )

    company = relationship("Company", back_populates="assets_liabilities")

class Equity(db.Model):
    __tablename__ = 'equities'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False, default=0.0)

    company = relationship("Company", back_populates="equities")

# =========================================================================
# 3. MASTER REGISTRY MODEL (Sits at bottom so all child tokens are loaded)
# =========================================================================

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abn_number = db.Column(db.String(20), nullable=True)
    tfn_number = db.Column(db.String(20), nullable=True)
    contact_person = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.Date, default=datetime.utcnow)

    # All relationships are now safely instantiated after dependent modules exist
    financial_records = relationship("FinancialRecord", back_populates="company", lazy=True)
    payroll_records = relationship("PayrollRecord", back_populates="company", lazy=True)
    assets_liabilities = relationship("AssetLiability", back_populates="company", lazy=True)
    equities = relationship("Equity", back_populates="company", lazy=True)
