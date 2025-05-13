import logging
from app import db
from app.models import AssetLiability  # Import models

def initialize_database(company_id=1, additional_accounts=None):
    """
    Initializes the database with default accounts and BAS fields for a given company.
    Allows additional accounts to be passed dynamically.
    """
    # Preloading account categories (assets, liabilities, equity)
    default_accounts = [
        {"category": "asset", "subcategory": "cash", "description": "Cash in hand", "amount": 0.0, "company_id": company_id},
        {"category": "asset", "subcategory": "accounts_receivable", "description": "Accounts Receivable", "amount": 0.0, "company_id": company_id},
        {"category": "asset", "subcategory": "inventory", "description": "Inventory", "amount": 0.0, "company_id": company_id},
        {"category": "liability", "subcategory": "accounts_payable", "description": "Accounts Payable", "amount": 0.0, "company_id": company_id},
        {"category": "liability", "subcategory": "short_term_loans", "description": "Short Term Loans", "amount": 0.0, "company_id": company_id},
        {"category": "equity", "subcategory": "retained_earnings", "description": "Retained Earnings", "amount": 0.0, "company_id": company_id},
        {"category": "equity", "subcategory": "contributed_capital", "description": "Contributed Capital", "amount": 0.0, "company_id": company_id},
    ]

    # Preloading BAS fields
    bas_fields = [
        {"category": "gst", "subcategory": "G1_total_sales", "description": "Total sales (G1)", "amount": 0.0, "company_id": company_id},
        {"category": "gst", "subcategory": "G2_export_sales", "description": "Export sales (G2)", "amount": 0.0, "company_id": company_id},
        {"category": "gst", "subcategory": "G3_gst_free_sales", "description": "Other GST-free sales (G3)", "amount": 0.0, "company_id": company_id},
        {"category": "gst", "subcategory": "G10_capital_purchases", "description": "Capital purchases (G10)", "amount": 0.0, "company_id": company_id},
        {"category": "gst", "subcategory": "G11_non_capital_purchases", "description": "Non-capital purchases (G11)", "amount": 0.0, "company_id": company_id},
        {"category": "payg", "subcategory": "W1_total_wages", "description": "Total salary, wages (W1)", "amount": 0.0, "company_id": company_id},
        {"category": "payg", "subcategory": "W2_payg_withholding", "description": "PAYG withholding (W2)", "amount": 0.0, "company_id": company_id},
        {"category": "payg", "subcategory": "T1_payg_income", "description": "PAYG instalment income (T1)", "amount": 0.0, "company_id": company_id},
    ]

    # Add additional accounts if provided
    if additional_accounts:
        default_accounts.extend(additional_accounts)

    # Add entries to the database
    try:
        for account in default_accounts + bas_fields:
            # Avoid duplicate entries
            if not AssetLiability.query.filter_by(
                category=account["category"],
                subcategory=account["subcategory"],
                company_id=company_id
            ).first():
                db.session.add(AssetLiability(**account))
        db.session.commit()
        logging.info("Database initialized successfully!")
    except Exception as e:
        logging.error(f"Error initializing database: {e}", exc_info=True)
