import logging
from flask import Flask, Blueprint, jsonify, request, render_template
from datetime import datetime
from app import db
from app.models import FinancialRecord, AssetLiability, Equity, Company

# Create a Blueprint for financial routes
financial_routes = Blueprint('financial_routes', __name__)

# Route: Profit and Loss Statement
@financial_routes.route('/profit_loss', methods=['GET'])
def profit_loss():
    """
    Generates a detailed Profit and Loss Statement, including address, all items, and totals.
    """
    try:
        logging.info("Checkpoint 1: Received query to /profit_loss route.")

        # Retrieve query parameters
        company_id = request.args.get('company_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        # Validate query parameters
        if not company_id or not date_from or not date_to:
            logging.warning("Checkpoint 2: Missing query parameters.")
            return jsonify({'error': 'Please provide company_id, date_from, and date_to.'}), 400

        # Query the company
        company = Company.query.filter_by(id=company_id).first()
        if not company:
            logging.warning(f"Checkpoint 3: Company with ID {company_id} not found.")
            return jsonify({'error': f'Company with ID {company_id} not found.'}), 404

        # Convert dates
        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
            logging.info(f"Checkpoint 4: Converted dates - date_from: {date_from}, date_to: {date_to}")
        except ValueError:
            logging.error("Checkpoint 4.1: Invalid date format.")
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        # Query financial records for itemized details
        logging.info("Checkpoint 5: Querying income, COGS, and expenses.")
        income_records = FinancialRecord.query.filter(
            FinancialRecord.company_id == company.id,
            FinancialRecord.date.between(date_from, date_to),
            FinancialRecord.type_of_income.isnot(None)
        ).all()
        total_income = sum(record.credit for record in income_records)

        cogs_records = FinancialRecord.query.filter(
            FinancialRecord.company_id == company.id,
            FinancialRecord.date.between(date_from, date_to),
            FinancialRecord.type_of_expense == "COGS"
        ).all()
        total_cogs = sum(record.debit for record in cogs_records)

        expense_records = FinancialRecord.query.filter(
            FinancialRecord.company_id == company.id,
            FinancialRecord.date.between(date_from, date_to),
            FinancialRecord.type_of_expense.isnot(None)
        ).filter(FinancialRecord.type_of_expense != "COGS").all()
        total_expenses = sum(record.debit for record in expense_records)

        # Calculate profits
        gross_profit = total_income - total_cogs
        operating_profit = gross_profit - total_expenses
        tax = operating_profit * 0.1  # Assume a 10% tax rate
        net_profit_after_tax = operating_profit - tax

        # Render HTML template
        logging.info("Checkpoint 6: Rendering detailed HTML template for Profit and Loss.")
        return render_template(
            'profit_loss.html',
            company_details={
                "name": company.name,
                "abn": company.abn_number,
                "address": company.address,  # Include address
                "period": {"from": str(date_from), "to": str(date_to)}
            },
            income_records=[{"description": r.description, "amount": r.credit} for r in income_records],
            total_income=total_income,
            cogs_records=[{"description": r.description, "amount": r.debit} for r in cogs_records],
            total_cogs=total_cogs,
            expense_records=[{"description": r.description, "amount": r.debit} for r in expense_records],
            total_expenses=total_expenses,
            gross_profit=gross_profit,
            operating_profit=operating_profit,
            tax=tax,
            net_profit_after_tax=net_profit_after_tax
        )

    except Exception as e:
        logging.error(f"Error generating Profit and Loss report: {e}", exc_info=True)
        return jsonify({'error': 'An error occurred while generating the report.'}), 500


# Route: Balance Sheet
@financial_routes.route('/balance_sheet', methods=['GET'])
def balance_sheet():
    """
    Generates a professional Balance Sheet, including address, all items, and calculations.
    """
    try:
        logging.info("Checkpoint 1: Received query to /balance_sheet route.")

        # Retrieve query parameters
        company_id = request.args.get('company_id')

        # Validate query parameters
        if not company_id:
            logging.warning("Checkpoint 2: Missing company_id parameter.")
            return jsonify({'error': 'Please provide company_id.'}), 400

        # Query the company
        company = Company.query.filter_by(id=company_id).first()
        if not company:
            logging.warning(f"Checkpoint 3: Company with ID {company_id} not found.")
            return jsonify({'error': f'Company with ID {company_id} not found.'}), 404

        # Query assets and liabilities
        logging.info("Checkpoint 4: Querying assets and liabilities.")
        assets = AssetLiability.query.filter_by(company_id=company_id, category="Asset").all()
        total_assets = sum(asset.amount for asset in assets)

        liabilities = AssetLiability.query.filter_by(company_id=company_id, category="Liability").all()
        total_liabilities = sum(liability.amount for liability in liabilities)

        # Calculate Equity
        equity = total_assets - total_liabilities
        logging.info(f"Calculated Equity: {equity}")

        # Render HTML template
        return render_template(
            'balance_sheet.html',
            company_details={
                "name": company.name,
                "abn": company.abn_number,
                "address": company.address  # Include address
            },
            assets=[{"subcategory": a.subcategory, "amount": a.amount} for a in assets],
            total_assets=total_assets,
            liabilities=[{"subcategory": l.subcategory, "amount": l.amount} for l in liabilities],
            total_liabilities=total_liabilities,
            equity=equity
        )

    except Exception as e:
        logging.error(f"Error generating Balance Sheet: {e}", exc_info=True)
        return jsonify({'error': 'An error occurred while generating the balance sheet.'}), 500
