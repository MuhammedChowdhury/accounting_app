import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, Invoice

invoice_routes = Blueprint('invoice_routes', __name__)

@invoice_routes.route('/add_invoice', methods=['GET'])
def add_invoice():
    """Renders the single entry manual invoicing layout."""
    company_id = request.args.get('company_id', type=int) or session.get('company_id')
    if not company_id:
        return redirect(url_for('company_routes.select_company'))
    company = db.session.get(Company, company_id)
    return render_template('add_invoice.html', company=company)

@invoice_routes.route('/view_invoices', methods=['GET', 'POST'])
def view_invoices():
    """Handles both invoice data submission rows and ledger list reading views."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        if request.method == 'POST':
            client_name = request.form.get('client_name')
            line_items = request.form.get('line_items')
            total_amount = request.form.get('total_amount', type=float, default=0.0)
            due_date_str = request.form.get('due_date')

            if client_name and total_amount:
                from datetime import datetime
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except Exception:
                    due_date = datetime.utcnow().date()

                new_invoice = Invoice(
                    client_name=client_name,
                    line_items=line_items,
                    total_amount=total_amount,
                    due_date=due_date,
                    payment_status='Pending'
                )
                db.session.add(new_invoice)
                db.session.commit()
                return redirect(url_for('invoice_routes.view_invoices', company_id=company_id))

        invoices = db.session.query(Invoice).all()
        return render_template('view_invoices.html', company=company, invoices=invoices)

    except Exception as e:
        logging.error(f"Invoicing module computation failure: {e}", exc_info=True)
        return jsonify({'error': 'Accounts receivable dataset failed to initialize.'}), 500
