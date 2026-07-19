import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, PurchaseOrder

purchase_order_routes = Blueprint('purchase_order_routes', __name__)

@purchase_order_routes.route('/add_purchase_order', methods=['GET', 'POST'])
def add_purchase_order():
    """Renders the PO issue layout or processes submissions securely."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))
        company = db.session.get(Company, company_id)

        if request.method == 'POST':
            supplier_name = request.form.get('supplier_name')
            line_items = request.form.get('line_items')
            total_amount = request.form.get('total_amount', type=float, default=0.0)
            shipping_address = request.form.get('shipping_address')

            if supplier_name and total_amount:
                new_po = PurchaseOrder(
                    supplier_name=supplier_name,
                    line_items=line_items,
                    total_amount=total_amount,
                    shipping_address=shipping_address,
                    payment_status='Pending'
                )
                db.session.add(new_po)
                db.session.commit()
                return redirect(url_for('purchase_order_routes.view_purchase_orders', company_id=company_id))

        return render_template('add_purchase_order.html', company=company)
    except Exception as e:
        logging.error(f"PO initialization engine failure: {e}", exc_info=True)
        return jsonify({'error': 'Procurement engine failure.'}), 500

@purchase_order_routes.route('/view_purchase_orders', methods=['GET'])
def view_purchase_orders():
    """Fetches procurement files logged in system memory maps."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        company = db.session.get(Company, company_id)
        purchase_orders = db.session.query(PurchaseOrder).all()
        return render_template('view_purchase_orders.html', company=company, purchase_orders=purchase_orders)
    except Exception as e:
        logging.error(f"PO history extraction error: {e}", exc_info=True)
        return jsonify({'error': 'Procurement database connection failure.'}), 500
