import logging
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from datetime import datetime
from app import db
from app.models import FinancialRecord, AssetLiability, Equity, Company

financial_routes = Blueprint('financial_routes', __name__)

@financial_routes.route('/profit_loss', methods=['GET'])
def profit_loss():
    """Generates detailed financial performance summaries."""
    try:
        company_id = request.args.get('company_id', type=int)
        date_from_raw = request.args.get('date_from')
        date_to_raw = request.args.get('date_to')

        if not company_id or not date_from_raw or not date_to_raw:
            return jsonify({'error': 'Missing identification parameters context keys.'}), 400

        company = db.session.get(Company, company_id)
        if not company:
            return jsonify({'error': 'Target business entity not logged.'}), 404

        try:
            date_from = datetime.strptime(date_from_raw, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to_raw, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid date format parameters. Use YYYY-MM-DD.'}), 400

        income_records = db.session.query(FinancialRecord).filter(
            FinancialRecord.company_id == company.id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to,
            FinancialRecord.type_of_income.isnot(None)
        ).all()
        total_income = sum((r.credit or 0.0) for r in income_records)

        cogs_records = db.session.query(FinancialRecord).filter(
            FinancialRecord.company_id == company.id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to,
            FinancialRecord.type_of_expense == "COGS"
        ).all()
        total_cogs = sum((r.debit or 0.0) for r in cogs_records)

        expense_records = db.session.query(FinancialRecord).filter(
            FinancialRecord.company_id == company.id,
            FinancialRecord.date >= date_from,
            FinancialRecord.date <= date_to,
            FinancialRecord.type_of_expense.isnot(None),
            FinancialRecord.type_of_expense != "COGS"
        ).all()
        total_expenses = sum((r.debit or 0.0) for r in expense_records)

        gross_profit = total_income - total_cogs
        operating_profit = gross_profit - total_expenses
        tax = max(0.0, operating_profit * 0.1)
        net_profit_after_tax = operating_profit - tax

        return render_template(
            'profit_loss.html',
            company_details={"name": company.name, "abn": company.abn_number, "address": company.address, "period": {"from": str(date_from), "to": str(date_to)}},
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
        logging.error(f"Error rendering financial position records: {e}", exc_info=True)
        return jsonify({'error': 'Failed to resolve ledger margins calculations.'}), 500


@financial_routes.route('/balance_sheet', methods=['GET'])
def balance_sheet():
    """Generates organizational positions assets and liabilities records sheets."""
    try:
        company_id = request.args.get('company_id', type=int)
        if not company_id:
            return jsonify({'error': 'Company identification parameters missing.'}), 400

        company = db.session.get(Company, company_id)
        if not company:
            return jsonify({'error': 'Corporate file context target unallocated.'}), 404

        assets = db.session.query(AssetLiability).filter_by(company_id=company.id, category="Asset").all()
        total_assets = sum((a.amount or 0.0) for a in assets)

        liabilities = db.session.query(AssetLiability).filter_by(company_id=company.id, category="Liability").all()
        total_liabilities = sum((l.amount or 0.0) for l in liabilities)
        equity = total_assets - total_liabilities

        return render_template(
            'balance_sheet.html',
            company_details={"name": company.name, "abn": company.abn_number, "address": company.address},
            assets=[{"subcategory": a.subcategory, "amount": a.amount} for a in assets],
            total_assets=float(total_assets),
            liabilities=[{"subcategory": l.subcategory, "amount": l.amount} for l in liabilities],
            total_liabilities=float(total_liabilities),
            equity=float(equity)
        )
    except Exception as e:
        logging.error(f"Error compiling statement sheet layout: {e}", exc_info=True)
        return jsonify({'error': 'Solvency processing failure.'}), 500
