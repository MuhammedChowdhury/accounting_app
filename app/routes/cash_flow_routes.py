import logging
from flask import Blueprint, request, render_template, jsonify
from app.models import FinancialRecord, Company
from app import db
from sqlalchemy import func
from datetime import datetime

cash_flow_routes = Blueprint("cash_flow_routes", __name__)

@cash_flow_routes.route('/cash_flow', methods=['GET'])
def cash_flow():
    company_id = request.args.get('company_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    # ✅ Ensure required parameters are provided
    if not company_id or not date_from or not date_to:
        return jsonify({"error": "Invalid input. Please provide company_id, date_from, and date_to."}), 400

    try:
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # ✅ Example Query (Adjust as Needed)
    total_cash_flow = db.session.query(func.sum(FinancialRecord.credit)).filter(
        FinancialRecord.company_id == company_id,
        FinancialRecord.date >= date_from,
        FinancialRecord.date <= date_to
    ).scalar() or 0.0

    return jsonify({"company_id": company_id, "total_cash_flow": total_cash_flow})
