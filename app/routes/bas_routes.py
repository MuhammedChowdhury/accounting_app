import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, FinancialRecord

bas_routes = Blueprint('bas_routes', __name__)

@bas_routes.route('/bas_form', methods=['GET'])
def bas_form():
    """Dynamically calculates standard GST obligations across active ledger entries."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        records = db.session.query(FinancialRecord).filter_by(company_id=company_id).all()

        # Dynamic accumulation of GST paid and received values
        gst_paid = sum(record.gst_paid or 0.0 for record in records)
        gst_received = sum(record.gst_received or 0.0 for record in records)
        net_bas_obligation = gst_received - gst_paid

        return render_template(
            'bas_form.html',
            company=company,
            gst_paid=gst_paid,
            gst_received=gst_received,
            net_bas_obligation=net_bas_obligation
        )
    except Exception as e:
        logging.error(f"BAS matrix calculation failure: {e}", exc_info=True)
        return jsonify({'error': 'BAS generation engine error.'}), 500
