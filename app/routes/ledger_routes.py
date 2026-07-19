import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, FinancialRecord

ledger_routes = Blueprint('ledger_routes', __name__)

@ledger_routes.route('/general_ledger_form', methods=['GET'])
def general_ledger_form():
    """Dynamically compiles chronological transaction arrays strictly for the active client."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        # Fetch every debit and credit line isolated to this specific client account
        records = db.session.query(FinancialRecord).filter_by(company_id=company_id).order_by(FinancialRecord.date.asc()).all()

        return render_template('general_ledger.html', company=company, records=records)
    except Exception as e:
        logging.error(f"General Ledger compilation failure: {e}", exc_info=True)
        return jsonify({'error': 'Ledger system failed to initialize.'}), 500
