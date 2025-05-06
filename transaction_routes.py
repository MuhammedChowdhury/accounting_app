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


# Route: Add Single Transaction
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


# Route: Bulk Import Transactions
@transaction_routes.route('/add_transaction_bulk', methods=['POST'])
def add_transaction_bulk():
    try:
        transactions = request.json.get('transactions', [])
        if not transactions or not isinstance(transactions, list):
            return render_template('bulk_transaction_error.html', error_message="Invalid input. Expected a list of transactions."), 400

        added_transactions = []
        skipped_transactions = []

        for transaction in transactions:
            try:
                if not transaction.get('date') or not transaction.get('description'):
                    skipped_transactions.append({
                        "transaction": transaction,
                        "reason": "Missing required fields: date or description."
                    })
                    continue

                try:
                    transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
                except ValueError:
                    skipped_transactions.append({
                        "transaction": transaction,
                        "reason": "Invalid date format. Use YYYY-MM-DD."
                    })
                    continue

                new_transaction = FinancialRecord(
                    date=transaction_date,
                    description=transaction['description'],
                    debit=float(transaction.get('debit', 0.0)),
                    credit=float(transaction.get('credit', 0.0)),
                    type_of_expense=transaction.get('type_of_expense', None),
                    type_of_income=transaction.get('type_of_income', None)
                )
                db.session.add(new_transaction)
                added_transactions.append(transaction['description'])

            except Exception as e:
                skipped_transactions.append({
                    "transaction": transaction,
                    "reason": f"Error: {str(e)}"
                })
                logging.error(f"Error adding transaction {transaction}: {e}", exc_info=True)

        db.session.commit()

        return render_template('bulk_transaction_success.html', added_transactions=added_transactions, skipped_transactions=skipped_transactions), 200

    except Exception as e:
        logging.error(f"General error in bulk transaction import: {e}", exc_info=True)
        return render_template('bulk_transaction_error.html', error_message="Failed to import transactions due to server error"), 500


# Route: Trial Balance
@transaction_routes.route('/trial_balance', methods=['GET'])
def trial_balance():
    try:
        company_id = request.args.get('company_id', type=int)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        if not company_id or not date_from or not date_to:
            return render_template('trial_balance_error.html', error_message="Invalid input. Please provide company_id, date_from, and date_to."), 400

        trial_balance_data = [
            {"account_name": "Cash", "debit": 1000.00, "credit": 0.00},
            {"account_name": "Accounts Payable", "debit": 0.00, "credit": 500.00},
        ]

        return render_template('trial_balance_result.html', company_id=company_id, trial_balance_data=trial_balance_data), 200

    except Exception as e:
        logging.error(f"Error generating trial balance: {e}", exc_info=True)
        return render_template('trial_balance_error.html', error_message="Failed to generate trial balance due to server error"), 500
