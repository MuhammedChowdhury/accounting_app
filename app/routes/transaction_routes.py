import os
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request, render_template
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app import db
from app.models import FinancialRecord, Company, AssetLiability
from io import StringIO
import csv



# Define the blueprint
transaction_routes = Blueprint('transaction_routes', __name__, template_folder="templates")

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
            transaction_date = datetime.strptime(date_str, '%d-%m-%Y')  # Changed format to DD-MM-YYYY
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use DD-MM-YYYY.'}), 400

        invoice_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            invoice_path = os.path.join(UPLOAD_FOLDER, filename)

        # ✅ Save Transaction to Database
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

        return render_template('transaction_success.html', description=description)

    except Exception as e:
        logging.error(f"Error adding transaction: {e}", exc_info=True)
        return render_template('transaction_error.html', error_message="Failed to add transaction due to server error"), 500

# ✅ Route: Bulk Import Transactions (POST)
@transaction_routes.route('/add_transaction_bulk', methods=['POST'])
def process_transaction_bulk():
    try:
        csv_raw = request.form.get('csv_data', '').strip()
        if not csv_raw:
            return render_template("bulk_transaction_error.html", error_message="No CSV data provided."), 400

        reader = csv.DictReader(StringIO(csv_raw))
        transactions = []

        for row in reader:
            try:
                transaction = FinancialRecord(
                    date=datetime.strptime(row["Date"], "%d-%m-%Y"),
                    description=row["Description"],
                    debit=float(row.get("Debit", 0) or 0),
                    credit=float(row.get("Credit", 0) or 0),
                    type_of_expense=row.get("Type of Expense"),
                    type_of_income=row.get("Type of Income")
                )
                db.session.add(transaction)
                transactions.append(transaction)
            except Exception as e:
                logging.error(f"Error processing row {row}: {e}", exc_info=True)

        db.session.commit()
        return render_template('bulk_transaction_form.html', transactions=transactions)

    except Exception as e:
        logging.error(f"Bulk transaction upload failed: {e}", exc_info=True)
        return render_template('bulk_transaction_error.html', error_message="Bulk upload failed."), 500
