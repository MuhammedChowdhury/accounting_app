from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
import logging
from datetime import datetime, timedelta
from app.models import db, PurchaseOrder, Bill

# Blueprint setup
purchase_order_routes = Blueprint('purchase_order_routes', __name__)

@purchase_order_routes.route('/add_purchase_order', methods=['GET', 'POST'])
def add_purchase_order():
    if request.method == 'POST':
        try:
            data = request.form
            order_number = data.get('order_number')
            supplier = data.get('supplier')
            line_items = data.get('line_items', "").split(",")  # Ensure list format
            total_amount = data.get('total_amount')
            delivery_date = data.get('delivery_date')

            # Validate required fields
            if not all([order_number, supplier, line_items, total_amount, delivery_date]):
                flash("Missing required fields", "error")
                return redirect(url_for('purchase_order_routes.add_purchase_order'))

            # Convert total amount safely
            try:
                total_amount = float(total_amount)
            except ValueError:
                flash("Invalid total amount format", "error")
                return redirect(url_for('purchase_order_routes.add_purchase_order'))

            # Create purchase order with initial status
            new_purchase_order = PurchaseOrder(
                order_number=order_number,
                supplier=supplier,
                line_items=line_items,
                total_amount=total_amount,
                delivery_date=delivery_date,
                status="Pending"
            )
            db.session.add(new_purchase_order)
            db.session.commit()

            flash("Purchase order added successfully!", "success")
            return redirect(url_for('purchase_order_routes.view_purchase_orders'))

        except Exception as e:
            logging.error(f"Error adding purchase order: {e}", exc_info=True)
            flash(f"Failed to add purchase order: {str(e)}", "error")
            return redirect(url_for('purchase_order_routes.add_purchase_order'))

    return render_template('add_purchase_order.html')

@purchase_order_routes.route('/view_purchase_orders', methods=['GET'])
def view_purchase_orders():
    try:
        purchase_orders = PurchaseOrder.query.all()
        return render_template('purchase_orders.html', purchase_orders=purchase_orders)
    except Exception as e:
        logging.error(f"Error fetching purchase orders: {e}", exc_info=True)
        flash(f"Failed to fetch purchase orders: {str(e)}", "error")
        return redirect(url_for('purchase_order_routes.view_purchase_orders'))

@purchase_order_routes.route('/convert_to_bill/<int:purchase_order_id>', methods=['POST'])
def convert_to_bill(purchase_order_id):
    try:
        purchase_order = PurchaseOrder.query.get(purchase_order_id)
        if not purchase_order:
            flash("Purchase order not found", "error")
            return redirect(url_for('purchase_order_routes.view_purchase_orders'))

        # Dynamically set due date to 30 days after purchase order creation
        due_date = datetime.today() + timedelta(days=30)

        # Create bill using purchase order details
        new_bill = Bill(
            vendor_name=purchase_order.supplier,
            line_items=purchase_order.line_items,
            total_amount=purchase_order.total_amount,
            due_date=due_date.strftime("%Y-%m-%d"),
            payment_status="Unpaid"
        )
        db.session.add(new_bill)

        # Mark purchase order as converted
        purchase_order.status = "Converted to Bill"
        db.session.commit()

        flash("Purchase order converted to bill successfully!", "success")
        return redirect(url_for('purchase_order_routes.view_purchase_orders'))
    except Exception as e:
        logging.error(f"Error converting purchase order: {e}", exc_info=True)
        flash(f"Failed to convert purchase order: {str(e)}", "error")
        return redirect(url_for('purchase_order_routes.view_purchase_orders'))
