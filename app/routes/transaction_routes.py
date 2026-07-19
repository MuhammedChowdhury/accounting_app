import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, FinancialRecord

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/add-transaction', methods=['GET', 'POST'])
def add_transaction():
    """ISSUE 1: Posts a single, manual journal entry row into the active client ledger."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        if request.method == 'POST':
            description = request.form.get('description')
            debit = request.form.get('debit', type=float, default=0.0)
            credit = request.form.get('credit', type=float, default=0.0)
            type_of_expense = request.form.get('type_of_expense')
            type_of_income = request.form.get('type_of_income')
            
            from datetime import datetime
            date_str = request.form.get('date')
            try:
                date_val = datetime.strptime(date_str, '%Y-%m-%d').date()
            except Exception:
                date_val = datetime.utcnow().date()

            if description:
                record = FinancialRecord(
                    date=date_val,
                    description=description,
                    debit=debit,
                    credit=credit,
                    type_of_expense=type_of_expense if debit > 0 else None,
                    type_of_income=type_of_income if credit > 0 else None,
                    company_id=company_id
                )
                db.session.add(record)
                db.session.commit()
                return redirect(url_for('index'))

        return render_template('add_transaction.html', company=company)
    except Exception as e:
        logging.error(f"Single entry posting crash: {e}", exc_info=True)
        return jsonify({'error': 'Journal posting failed.'}), 500


@transaction_routes.route('/add-transaction-bulk', methods=['GET', 'POST'])
def add_transaction_bulk():
    """ISSUE 2: Ingests a raw streaming CSV block of rows straight into ledger tables."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        if request.method == 'POST':
            csv_data = request.form.get('csv_data')
            if csv_data:
                from datetime import datetime
                lines = csv_data.strip().split('\n')
                
                # Skip header row if present
                start_index = 1 if "Date" in lines[0] else 0
                
                for line in lines[start_index:]:
                    parts = line.split(',')
                    if len(parts) >= 4:
                        try:
                            date_val = datetime.strptime(parts[0].strip(), '%d-%m-%Y').date()
                        except Exception:
                            date_val = datetime.utcnow().date()
                            
                        desc = parts[1].strip()
                        deb = float(parts[2].strip() or 0.0)
                        cred = float(parts[3].strip() or 0.0)
                        exp_t = parts[4].strip() if len(parts) > 4 else None
                        inc_t = parts[5].strip() if len(parts) > 5 else None

                        record = FinancialRecord(
                            date=date_val,
                            description=desc,
                            debit=deb,
                            credit=cred,
                            type_of_expense=exp_t if deb > 0 else None,
                            type_of_income=inc_t if cred > 0 else None,
                            company_id=company_id
                        )
                        db.session.add(record)
                
                db.session.commit()
                return redirect(url_for('index'))

        return render_template('bulk_transaction_form.html', company=company)
    except Exception as e:
        logging.error(f"Bulk data ingest processing crash: {e}", exc_info=True)
        return jsonify({'error': 'Batch migration failed.'}), 500


@transaction_routes.route('/trial-balance', methods=['GET'])
def trial_balance():
    """Audits balanced totals rows across active client account pools dynamically."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        records = db.session.query(FinancialRecord).filter_by(company_id=company_id).all()

        total_debits = sum(record.debit or 0.0 for record in records)
        total_credits = sum(record.credit or 0.0 for record in records)

        return render_template(
            'trial_balance.html',
            company=company,
            total_debits=total_debits,
            total_credits=total_credits,
            is_balanced=(round(total_debits, 2) == round(total_credits, 2))
        )
    except Exception as e:
        logging.error(f"Trial Balance engine error: {e}", exc_info=True)
        return jsonify({'error': 'Trial balance calculation failed.'}), 500
