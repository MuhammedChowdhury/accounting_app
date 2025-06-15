import logging
from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import func
from app import db
from app.models import FinancialRecord

# Define the blueprint
cash_flow_routes = Blueprint('cash_flow_routes', __name__)

# Route: Cash Flow Form
@cash_flow_routes.route('/cash_flow_form', methods=['GET'])
def cash_flow_form():
    """
    Renders the form for generating a cash flow statement.
    """
    return render_template('cash_flow_form.html')

# Route: Generate Cash Flow Statement
@cash_flow_routes.route('/cash_flow', methods=['GET'])
def cash_flow():
    """
    Generates a cash flow statement for a given company and date range.
    """
    try:
        company_id = request.args.get('company_id', type=int)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        if not company_id or not date_from or not date_to:
            return jsonify({'error': 'Invalid input. Please provide company_id, date_from, and date_to.'}), 400

        # Query the database for cash flow data
        inflow = db.session.query(func.sum(FinancialRecord.credit)).filter(
            FinancialRecord.company_id == company_id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to,
            FinancialRecord.type_of_income.isnot(None)
        ).scalar() or 0.0

        outflow = db.session.query(func.sum(FinancialRecord.debit)).filter(
            FinancialRecord.company_id == company_id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to,
            FinancialRecord.type_of_expense.isnot(None)
        ).scalar() or 0.0

        net_cash_flow = inflow - outflow

        # Render the result in HTML
        return render_template(
            'cash_flow_result.html',
            company_id=company_id,
            date_from=date_from,
            date_to=date_to,
            cash_inflow=inflow,
            cash_outflow=outflow,
            net_cash_flow=net_cash_flow
        ), 200

    except Exception as e:
        logging.error(f"Error generating cash flow statement: {e}", exc_info=True)
        return jsonify({'error': 'Failed to generate cash flow statement'}), 500
