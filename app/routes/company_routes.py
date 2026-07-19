import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company

# Safe blueprint boundary definition
company_routes = Blueprint('company_routes', __name__)

@company_routes.route('/dashboard')
def dashboard():
    """Main practice landing layout. Ensures a client database ID is locked into the session."""
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_routes.select_company'))
    return render_template('welcome.html')

@company_routes.route('/Company_Form', methods=['GET', 'POST'])
def company_form():
    """Registers a fresh business record to isolate books for different practice clients."""
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            abn_number = request.form.get('abn_number')
            contact_person = request.form.get('contact_person')
            address = request.form.get('address')

            if not name or not abn_number:
                return jsonify({'error': 'Company Name and ABN records are mandatory.'}), 400

            company = db.session.query(Company).filter_by(name=name).first()
            if not company:
                company = Company(
                    name=name,
                    abn_number=abn_number,
                    contact_person=contact_person,
                    address=address
                )
                db.session.add(company)
                db.session.commit()

            session['company_id'] = company.id
            return redirect(url_for('company_routes.dashboard'))

        return render_template('Company_Form.html')
    except Exception as e:
        logging.error(f"Error executing client onboarding data: {e}", exc_info=True)
        return jsonify({'error': f'Could not complete initialization: {str(e)}'}), 500

@company_routes.route('/select_company', methods=['GET', 'POST'])
def select_company():
    """Client switchboard screen to cycle between different active bookkeeping ledgers."""
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            abn_number = request.form.get('abn_number')

            if not name or not abn_number:
                return jsonify({'error': 'Name and unique ABN inputs are required.'}), 400

            company = db.session.query(Company).filter_by(name=name).first()
            if not company:
                company = Company(
                    name=name, 
                    abn_number=abn_number, 
                    contact_person=request.form.get('contact_person'), 
                    address=request.form.get('address')
                )
                db.session.add(company)
                db.session.commit()

            session['company_id'] = company.id
            return redirect(url_for('company_routes.dashboard'))

        companies = db.session.query(Company).all()
        return render_template('select_company.html', companies=companies)
    except Exception as e:
        logging.error(f"Error connecting company selector records: {e}", exc_info=True)
        return jsonify({'error': 'Selection registry failed.'}), 500
