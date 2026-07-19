import logging
from flask import Blueprint, render_template, jsonify

report_routes = Blueprint('report_routes', __name__)

@report_routes.route('/report/profit_loss', methods=['GET'])
def profit_loss_report():
    """Generates an isolated sandbox simulation P&L calculation array."""
    try:
        company_details = {
            "name": "Demo Evaluation Sandbox Company Pty Ltd",
            "address": "123 Business Street, Sydney, NSW, Australia",
            "abn": "12345678901",
            "period": {"from": "2025-01-01", "to": "2025-12-31"},
        }

        data = {
            "income": [{"description": "Sales Revenue Analysis", "amount": 50000.00}],
            "cogs": [{"description": "Opening Materials Stock", "amount": 10000.00}],
            "expenses": [{"description": "Operational Corporate Overhead Allocation", "amount": 8000.00}],
            "tax": 4000.00
        }

        total_income = sum(item["amount"] for item in data["income"])
        total_cogs = sum(item["amount"] for item in data["cogs"])
        gross_profit = total_income - total_cogs
        total_expenses = sum(item["amount"] for item in data["expenses"])
        operating_profit = gross_profit - total_expenses
        net_profit_after_tax = operating_profit - data["tax"]

        return render_template(
            'profit_loss.html',
            company_details=company_details,
            income_records=data["income"],
            total_income=total_income,
            cogs_records=data["cogs"],
            total_cogs=total_cogs,
            expense_records=data["expenses"],
            total_expenses=total_expenses,
            gross_profit=gross_profit,
            operating_profit=operating_profit,
            tax=data["tax"],
            net_profit_after_tax=net_profit_after_tax
        )
    except Exception as e:
        logging.error(f"Error parsing sample demonstration layout: {e}", exc_info=True)
        return jsonify({'error': 'Sandbox compilation failure.'}), 500
