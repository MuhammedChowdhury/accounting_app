import logging
from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import func
from app import db
from app.models import FinancialRecord

# Define the blueprint
ledger_routes = Blueprint('ledger_routes', __name__)

# Route: General Ledger Form
@ledger_routes.route('/general_ledger_form', methods=['GET'])
def general_ledger_form():
    """
    Renders the form for generating a general ledger.
    """
    return render_template('general_ledger_form.html')

# Route: Generate General Ledger Report
@ledger_routes.route('/general_ledger', methods=['GET'])
def general_ledger():
    """
    Generates a general ledger for a given company and date range.
    """
    try:
        company_id = request.args.get('company_id', type=int)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        if not company_id or not date_from or not date_to:
            return jsonify({'error': 'Invalid input. Please provide company_id, date_from, and date_to.'}), 400

        # Query the database for ledger data
        ledger_entries = FinancialRecord.query.filter(
            FinancialRecord.company_id == company_id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to
        ).order_by(FinancialRecord.date.asc()).all()

        # Render the ledger entries in HTML
        return render_template(
            'general_ledger_result.html',
            company_id=company_id,
            date_from=date_from,
            date_to=date_to,
            ledger_entries=ledger_entries
        )

    except Exception as e:
        logging.error(f"Error generating general ledger: {e}", exc_info=True)
        return jsonify({'error': 'Failed to generate general ledger'}), 500
