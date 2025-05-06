from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric, CheckConstraint
from datetime import datetime

# Model: FinancialRecord
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
    invoice = db.Column(db.String(255), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    # Relationships
    company = relationship("Company", back_populates="financial_records")

# Model: PayrollRecord
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

    # Relationships
    company = relationship("Company", back_populates="payroll_records")

# Model: AssetLiability
class AssetLiability(db.Model):
    __tablename__ = 'assets_liabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False, default=0.0)

    # Explicitly named Check Constraint
    __table_args__ = (
        CheckConstraint("category IN ('Asset', 'Liability')", name="ck_asset_liability_category"),
    )

    # Relationships
    company = relationship("Company", back_populates="assets_liabilities")

# Model: Equity
class Equity(db.Model):
    __tablename__ = 'equities'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(Numeric(10, 2), nullable=False, default=0.0)

    # Relationships
    company = relationship("Company", back_populates="equities")

# Model: Quote
class Quote(db.Model):
    __tablename__ = 'quotes'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    validity_period = db.Column(db.Date, nullable=False)

# Model: Invoice
class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), default='Pending')

# Model: PurchaseOrder
class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    payment_status = db.Column(db.String(50), default='Pending')

# Model: Bill
class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(255), nullable=False)
    line_items = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), default='Unpaid')

# Model: Company
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

    # Relationships
    financial_records = relationship("FinancialRecord", back_populates="company", lazy=True)
    payroll_records = relationship("PayrollRecord", back_populates="company", lazy=True)
    assets_liabilities = relationship("AssetLiability", back_populates="company", lazy=True)
    equities = relationship("Equity", back_populates="company", lazy=True)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
