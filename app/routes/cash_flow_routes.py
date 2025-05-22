import logging
from flask import Blueprint, request, render_template, jsonify
from app.models import FinancialRecord, Company
from app import db
from sqlalchemy import func
from datetime import datetime

cash_flow_routes = Blueprint("cash_flow_routes", __name__)

@cash_flow_routes.route('/cash_flow', methods=['GET', 'POST'])
def cash_flow():
    if request.method == 'POST':
        company_id = request.form.get('company_id')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')

        # ✅ Ensure required parameters are provided
        if not company_id or not date_from or not date_to:
            return jsonify({"error": "Invalid input. Please provide company_id, date_from, and date_to."}), 400

        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # ✅ Fetch Cash Inflow (Credits) & Cash Outflow (Debits)
        total_cash_inflow = db.session.query(func.sum(FinancialRecord.credit)).filter(
            FinancialRecord.company_id == company_id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to
        ).scalar() or 0.0

        total_cash_outflow = db.session.query(func.sum(FinancialRecord.debit)).filter(
            FinancialRecord.company_id == company_id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to
        ).scalar() or 0.0

        net_cash_flow = total_cash_inflow - total_cash_outflow

        return render_template("cash_flow_statement.html", 
                               company_id=company_id, 
                               date_from=date_from.strftime("%Y-%m-%d"), 
                               date_to=date_to.strftime("%Y-%m-%d"),
                               cash_inflow=total_cash_inflow, 
                               cash_outflow=total_cash_outflow, 
                               net_cash_flow=net_cash_flow)

    # Render form if accessing via GET
    return render_template("cash_flow_form.html")
