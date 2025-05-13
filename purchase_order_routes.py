from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import db, PurchaseOrder, Bill

# Blueprint setup
purchase_order_routes = Blueprint('purchase_order_routes', __name__)

@purchase_order_routes.route('/add_purchase_order', methods=['GET', 'POST'])
def add_purchase_order():
    if request.method == 'POST':
        try:
            data = request.form
            supplier_name = data.get('supplier_name')
            line_items = data.get('line_items')
            total_amount = data.get('total_amount')
            shipping_address = data.get('shipping_address')

            # Validate required fields
            if not supplier_name or not line_items or not total_amount or not shipping_address:
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
                supplier_name=supplier_name,
                line_items=line_items,
                total_amount=total_amount,
                shipping_address=shipping_address,
                status="Pending"
            )
            db.session.add(new_purchase_order)
            db.session.commit()

            flash("Purchase order added successfully!", "success")
            return redirect(url_for('purchase_order_routes.view_purchase_orders'))
        except Exception as e:
            flash(f"Failed to add purchase order: {str(e)}", "error")
            return redirect(url_for('purchase_order_routes.add_purchase_order'))

    return render_template('add_purchase_order.html')

@purchase_order_routes.route('/view_purchase_orders', methods=['GET'])
def view_purchase_orders():
    try:
        purchase_orders = PurchaseOrder.query.all()
        return render_template('view_purchase_orders.html', purchase_orders=purchase_orders)
    except Exception as e:
        flash(f"Failed to fetch purchase orders: {str(e)}", "error")
        return redirect(url_for('purchase_order_routes.view_purchase_orders'))

@purchase_order_routes.route('/convert_to_bill/<int:purchase_order_id>', methods=['POST'])
def convert_to_bill(purchase_order_id):
    try:
        purchase_order = PurchaseOrder.query.get(purchase_order_id)
        if not purchase_order:
            flash("Purchase order not found", "error")
            return redirect(url_for('purchase_order_routes.view_purchase_orders'))

        # Create bill using purchase order details
        new_bill = Bill(
            vendor_name=purchase_order.supplier_name,
            line_items=purchase_order.line_items,
            total_amount=purchase_order.total_amount,
            due_date='2025-05-15',  # Adjust based on business rules
            payment_status="Unpaid"
        )
        db.session.add(new_bill)

        # Mark purchase order as converted
        purchase_order.status = "Converted to Bill"
        db.session.commit()

        flash("Purchase order converted to bill successfully!", "success")
        return redirect(url_for('purchase_order_routes.view_purchase_orders'))
    except Exception as e:
        flash(f"Failed to convert purchase order: {str(e)}", "error")
        return redirect(url_for('purchase_order_routes.view_purchase_orders'))
