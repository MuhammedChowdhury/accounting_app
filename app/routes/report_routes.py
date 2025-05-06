import logging
from flask import Blueprint, render_template, jsonify

# Define the Blueprint
report_routes = Blueprint('report_routes', __name__)
logging.info("Blueprint 'report_routes' created.")

@report_routes.route('/profit_loss', methods=['GET'])
def profit_loss_report():
    """
    Generates a formatted Profit and Loss Statement including company details and reporting period.
    """
    try:
        # Log that the endpoint was accessed
        logging.info("Accessed the Profit and Loss Report endpoint.")

        # Simulate dynamic data (replace with actual database queries in production)
        company_details = {
            "name": "Example Company Pty Ltd",
            "address": "123 Business Street, Sydney, NSW, Australia",
            "abn": "12345678901",
            "period": {"from": "2025-01-01", "to": "2025-12-31"},
        }

        data = {
            "income": [
                {"description": "Sales Revenue", "amount": 50000.00},
                {"description": "Service Revenue", "amount": 20000.00},
                {"description": "Other Income", "amount": 3000.00},
            ],
            "cogs": [
                {"description": "Opening Inventory", "amount": 10000.00},
                {"description": "Purchases", "amount": 15000.00},
                {"description": "Direct Costs", "amount": 5000.00},
                {"description": "Closing Inventory", "amount": -8000.00},
            ],
            "expenses": [
                {"description": "Rent Expense", "amount": 8000.00},
                {"description": "Utilities Expense", "amount": 2000.00},
                {"description": "Payroll Expense", "amount": 12000.00},
                {"description": "Marketing Expense", "amount": 4000.00},
            ],
            "other_income_expenses": [
                {"description": "Gain on Asset Sale", "amount": 2000.00},
                {"description": "Loss on Asset Sale", "amount": -500.00},
            ],
            "tax": 5000.00,
        }

        # Calculate totals
        total_income = sum(item["amount"] for item in data["income"])
        total_cogs = sum(item["amount"] for item in data["cogs"])
        gross_profit = total_income - total_cogs

        total_expenses = sum(item["amount"] for item in data["expenses"])
        operating_profit = gross_profit - total_expenses

        total_other_income_expenses = sum(item["amount"] for item in data["other_income_expenses"])
        net_profit_before_tax = operating_profit + total_other_income_expenses
        net_profit_after_tax = net_profit_before_tax - data["tax"]

        # Log calculations
        logging.info(f"Total Income: {total_income}, Total COGS: {total_cogs}, Gross Profit: {gross_profit}")
        logging.info(f"Total Expenses: {total_expenses}, Operating Profit: {operating_profit}")
        logging.info(f"Net Profit Before Tax: {net_profit_before_tax}, Net Profit After Tax: {net_profit_after_tax}")

        # Pass calculated data and company details to the template
        return render_template(
            'profit_loss.html',
            company_details=company_details,
            income=data["income"],
            cogs=data["cogs"],
            expenses=data["expenses"],
            other_income_expenses=data["other_income_expenses"],
            total_income=total_income,
            total_cogs=total_cogs,
            gross_profit=gross_profit,
            total_expenses=total_expenses,
            operating_profit=operating_profit,
            total_other_income_expenses=total_other_income_expenses,
            net_profit_before_tax=net_profit_before_tax,
            tax=data["tax"],
            net_profit_after_tax=net_profit_after_tax
        )
    except Exception as e:
        logging.error(f"Error generating Profit and Loss Statement: {e}")
        return jsonify({'error': 'Failed to generate Profit and Loss Statement'}), 500
