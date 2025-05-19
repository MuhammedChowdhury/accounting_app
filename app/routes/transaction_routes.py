import os
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request, render_template
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app import db
from app.models import FinancialRecord, Company, AssetLiability

# Define the blueprint
transaction_routes = Blueprint('transaction_routes', __name__)

# Configure Uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads', 'invoices')
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Route: Display Form for Adding Transactions (GET)
@transaction_routes.route('/add-transaction', methods=['GET'])
def add_transaction_form():
    return render_template("add_transaction.html")

# ✅ Route: Display Bulk Transaction Import Form (GET)
@transaction_routes.route('/add-transaction-bulk', methods=['GET'])
def add_transaction_bulk_form():
    return render_template("bulk_transaction_form.html")

# ✅ Route: Display Trial Balance Page (GET)
@transaction_routes.route('/trial-balance', methods=['GET'])
def trial_balance_page():
    return render_template("trial_balance.html")

# ✅ Route: Add Single Transaction (POST)
@transaction_routes.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        description = request.form.get('description')
        debit = request.form.get('debit', 0.0)
        credit = request.form.get('credit', 0.0)
        date_str = request.form.get('date')
        type_of_expense = request.form.get('type_of_expense', None)
        type_of_income = request.form.get('type_of_income', None)
        file = request.files.get('invoice')

        if not description or not date_str:
            return jsonify({'error': 'Description and date are required fields.'}), 400

        try:
            transaction_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        invoice_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            invoice_path = os.path.join(UPLOAD_FOLDER, filename)

        new_transaction = FinancialRecord(
            date=transaction_date,
            description=description,
            debit=float(debit),
            credit=float(credit),
            type_of_expense=type_of_expense,
            type_of_income=type_of_income,
            invoice=invoice_path
        )
        db.session.add(new_transaction)
        db.session.commit()

        return render_template('transaction_success.html', description=description), 201

    except Exception as e:
        logging.error(f"Error adding transaction: {e}", exc_info=True)
        return render_template('transaction_error.html', error_message="Failed to add transaction due to server error"), 500
