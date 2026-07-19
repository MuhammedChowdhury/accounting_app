import logging
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.models import db, FinancialRecord, Company
from datetime import datetime
from sqlalchemy import func

cash_flow_routes = Blueprint('cash_flow_routes', __name__)

@cash_flow_routes.route('/cash_flow_form', methods=['GET'])
def cash_flow_form():
    """Renders the setups selection dashboard."""
    return render_template('cash_flow_form.html')


@cash_flow_routes.route('/cash_flow', methods=['GET', 'POST'])
def cash_flow():
    """Calculates operational fund movements."""
    try:
        company_id = request.form.get('company_id', request.args.get('company_id', type=int))
        date_from_raw = request.form.get('date_from', request.args.get('date_from'))
        date_to_raw = request.form.get('date_to', request.args.get('date_to'))

        if not company_id:
            flash("⚠ Please select a valid operating entity.")
            return redirect(url_for('cash_flow_routes.cash_flow_form'))

        company = db.session.get(Company, int(company_id))
        if not company:
            return jsonify({"error": "Company profile not found."}), 404

        date_from = datetime.strptime(date_from_raw, '%Y-%m-%d').date() if date_from_raw else None
        date_to = datetime.strptime(date_to_raw, '%Y-%m-%d').date() if date_to_raw else None

        base_query = db.session.query(FinancialRecord).filter(FinancialRecord.company_id == company.id)
        if date_from:
            base_query = base_query.filter(FinancialRecord.date >= date_from)
        if date_to:
            base_query = base_query.filter(FinancialRecord.date <= date_to)

        total_inflows = base_query.with_entities(func.sum(FinancialRecord.credit)).scalar() or 0.0
        total_outflows = base_query.with_entities(func.sum(FinancialRecord.debit)).scalar() or 0.0
        net_cash_flow = total_inflows - total_outflows

        statement = {
            "company_name": company.name,
            "period": {
                "start": str(date_from) if date_from else "Inception",
                "end": str(date_to) if date_to else "Present"
            },
            "metrics": {
                "total_inflows": float(total_inflows),
                "total_outflows": float(total_outflows),
                "net_cash_flow": float(net_cash_flow)
            }
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.args.get('json') == 'true':
            return jsonify(statement), 200

        return render_template('cash_flow.html', statement=statement)

    except ValueError:
        flash("⚠ Invalid date format criteria. Use YYYY-MM-DD.")
        return redirect(url_for('cash_flow_routes.cash_flow_form'))
    except Exception as e:
        logging.error(f"Critical metrics variance in cash flow engine: {e}", exc_info=True)
        return jsonify({"error": "Internal ledger tracking error."}), 500
