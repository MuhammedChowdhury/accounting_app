from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models import db, Bill
from datetime import datetime

bill_routes = Blueprint('bill_routes', __name__)

### 🔹 Add a Bill ###
@bill_routes.route('/add_bill', methods=['POST'])
def add_bill():
    """Receives bill data and saves it to the database."""
    try:
        data = request.form
        vendor_name = data.get('vendor_name')
        line_items = data.get('line_items')
        total_amount = float(data.get('total_amount'))
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d')

        new_bill = Bill(
            vendor_name=vendor_name,
            line_items=line_items,
            total_amount=total_amount,
            due_date=due_date,
            payment_status="Unpaid"  # Default status
        )
        db.session.add(new_bill)
        db.session.commit()

        return jsonify({'message': '✅ Bill added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to add bill: {str(e)}'}), 500

### 🔹 View All Bills (HTML) ###
@bill_routes.route('/view_bills', methods=['GET'])
def view_bills():
    """Displays bills in an HTML template."""
    try:
        bills = Bill.query.all()
        return render_template('bills.html', bills=bills)
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to fetch bills: {str(e)}'}), 500

### 🔹 View All Bills (JSON) ###
@bill_routes.route('/api/bills', methods=['GET'])
def get_bills():
    """Returns all bills in JSON format."""
    try:
        bills = Bill.query.all()
        return jsonify([{
            'id': bill.id,
            'vendor_name': bill.vendor_name,
            'line_items': bill.line_items,
            'total_amount': bill.total_amount,
            'due_date': bill.due_date.strftime('%Y-%m-%d'),
            'payment_status': bill.payment_status
        } for bill in bills]), 200
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to fetch bills: {str(e)}'}), 500

### 🔹 Update Bill Payment Status ###
@bill_routes.route('/update_bill/<int:bill_id>', methods=['POST'])
def update_bill(bill_id):
    """Updates the payment status of a bill."""
    try:
        bill = Bill.query.get(bill_id)
        if not bill:
            return jsonify({'error': '⚠ Bill not found!'}), 404

        bill.payment_status = request.form.get('payment_status', bill.payment_status)
        db.session.commit()

        return jsonify({'message': f'✅ Bill {bill_id} updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to update bill: {str(e)}'}), 500

### 🔹 Delete a Bill ###
@bill_routes.route('/delete_bill/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    """Deletes a bill from the database."""
    try:
        bill = Bill.query.get(bill_id)
        if not bill:
            return jsonify({'error': '⚠ Bill not found!'}), 404

        db.session.delete(bill)
        db.session.commit()

        return jsonify({'message': f'✅ Bill {bill_id} deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to delete bill: {str(e)}'}), 500
