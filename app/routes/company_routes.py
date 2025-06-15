import logging
from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Company

# Create Blueprint
company_routes = Blueprint('company_routes', __name__)

# Route to render the Company_Form.html
@company_routes.route('/Company_Form', methods=['GET', 'POST'])
def company_form():
    """
    Handles entering and verifying company details.
    """
    try:
        if request.method == 'POST':
            # Extract submitted company details
            name = request.form.get('name')
            abn_number = request.form.get('abn_number')
            contact_person = request.form.get('contact_person')
            address = request.form.get('address')

            # Validate required fields
            missing_fields = []
            if not name or not contact_person:
                missing_fields.append('name/contact_person')

            if missing_fields:
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

            # Check if the company exists or add it
            company = Company.query.filter_by(name=name).first()
            if not company:
                company = Company(
                    name=name,
                    abn_number=abn_number,
                    contact_person=contact_person,
                    address=address
                )
                db.session.add(company)
                db.session.commit()

            # Redirect to dashboard
            return redirect(f'/company_dashboard?company_id={company.id}')

        return render_template('Company_Form.html')
    except Exception as e:
        logging.error(f"Error in company form: {e}", exc_info=True)
        return jsonify({'error': f'Could not process the form: {str(e)}'}), 500

#  company dashboard
@company_routes.route('/company_dashboard', methods=['GET'])
def company_dashboard():
    """
    Displays the company dashboard.
    """
    try:
        # Manually query Company with ID 1 for testing
        company_id = request.args.get('company_id', type=int)

        company = Company.query.filter_by(id=company_id).first()

        # Add debugging test for Company ID 1
        test_company = Company.query.filter_by(id=1).first()
        if test_company:
            logging.info(f"Test Company Query: {test_company.name}, ID: {test_company.id}")

        if not company:
            return jsonify({'error': f'Company with ID {company_id} not found.'}), 404

        # Render template with company details
        return render_template('company_dashboard.html', company=company)

    except Exception as e:
        logging.error(f"Error in /company_dashboard route: {e}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred.'}), 500


# select company
@company_routes.route('/select_company', methods=['GET', 'POST'])
def select_company():
    """
    Allows users to select or add a company.
    """
    try:
        if request.method == 'POST':
            # Extract submitted company details
            name = request.form.get('name')
            abn_number = request.form.get('abn_number')
            contact_person = request.form.get('contact_person')
            address = request.form.get('address')

            # Validate required fields
            missing_fields = []
            if not name or not abn_number:
                missing_fields.append('Company Name/ABN Number')

            if missing_fields:
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

            # Check if the company already exists
            company = Company.query.filter_by(name=name).first()
            if not company:
                company = Company(
                    name=name,
                    abn_number=abn_number,
                    contact_person=contact_person,
                    address=address
                )
                db.session.add(company)
                db.session.commit()

            return redirect(url_for('company_routes.company_dashboard', company_id=company.id))


        # Query existing companies for selection
        companies = Company.query.all()
        return render_template('select_company.html', companies=companies)

    except Exception as e:
        logging.error(f"Error in select_company route: {e}", exc_info=True)
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


