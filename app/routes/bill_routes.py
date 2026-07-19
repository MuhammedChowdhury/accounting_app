import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, Bill

bill_routes = Blueprint('bill_routes', __name__)

@bill_routes.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    """Renders the invoice entry layout form or handles direct submissions."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))
        company = db.session.get(Company, company_id)
        
        if request.method == 'POST':
            vendor_name = request.form.get('vendor_name')
            line_items = request.form.get('line_items')
            total_amount = request.form.get('total_amount', type=float, default=0.0)
            due_date_str = request.form.get('due_date')

            if vendor_name and total_amount:
                from datetime import datetime
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except Exception:
                    due_date = datetime.utcnow().date()

                new_bill = Bill(
                    vendor_name=vendor_name,
                    line_items=line_items,
                    total_amount=total_amount,
                    due_date=due_date,
                    payment_status='Unpaid'
                )
                db.session.add(new_bill)
                db.session.commit()
                return redirect(url_for('bill_routes.view_bills', company_id=company_id))

        return render_template('add_bill.html', company=company)
    except Exception as e:
        logging.error(f"Error loading manual bill entry layout form: {e}", exc_info=True)
        return jsonify({'error': 'Internal configuration entry failed.'}), 500

@bill_routes.route('/view_bills', methods=['GET', 'POST'])
def view_bills():
    """Handles both bill data submission rows and ledger list reading views."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        if request.method == 'POST':
            vendor_name = request.form.get('vendor_name')
            line_items = request.form.get('line_items')
            total_amount = request.form.get('total_amount', type=float, default=0.0)
            due_date_str = request.form.get('due_date')

            if vendor_name and total_amount:
                from datetime import datetime
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except Exception:
                    due_date = datetime.utcnow().date()

                new_bill = Bill(
                    vendor_name=vendor_name,
                    line_items=line_items,
                    total_amount=total_amount,
                    due_date=due_date,
                    payment_status='Unpaid'
                )
                db.session.add(new_bill)
                db.session.commit()
                return redirect(url_for('bill_routes.view_bills', company_id=company_id))

        bills = db.session.query(Bill).all()
        return render_template('view_bills.html', company=company, bills=bills)

    except Exception as e:
        logging.error(f"Accounts payable matrix failure: {e}", exc_info=True)
        return jsonify({'error': 'Supplier liability engine failed to load.'}), 500
