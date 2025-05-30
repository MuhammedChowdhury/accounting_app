import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
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
            if not name or not contact_person:
                flash("Missing required fields: Name and Contact Person are mandatory.", "error")
                return redirect(url_for('company_routes.company_form'))

            # Check if the company exists, otherwise add it
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

                flash("Company registered successfully!", "success")

            return redirect(url_for('company_routes.company_dashboard', company_id=company.id))

        return render_template('Company_Form.html')

    except Exception as e:
        logging.error(f"Error in company form: {e}", exc_info=True)
        flash(f"Could not process the form: {str(e)}", "error")
        return redirect(url_for('company_routes.company_form'))

# Company Dashboard
@company_routes.route('/company_dashboard', methods=['GET'])
def company_dashboard():
    """
    Displays the company dashboard.
    """
    try:
        company_id = request.args.get('company_id', type=int)
        if not company_id:
            flash("Missing company ID parameter.", "error")
            return redirect(url_for('company_routes.select_company'))

        company = Company.query.filter_by(id=company_id).first()
        if not company:
            flash(f"Company with ID {company_id} not found.", "error")
            return redirect(url_for('company_routes.select_company'))

        return render_template('company_dashboard.html', company=company)

    except Exception as e:
        logging.error(f"Error in /company_dashboard route: {e}", exc_info=True)
        flash("An unexpected error occurred while loading the dashboard.", "error")
        return redirect(url_for('company_routes.select_company'))

# Select Company
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
            if not name or not abn_number:
                flash("Company Name and ABN Number are required.", "error")
                return redirect(url_for('company_routes.select_company'))

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

                flash("Company successfully added!", "success")

            return redirect(url_for('company_routes.company_dashboard', company_id=company.id))

        # Query existing companies for selection
        companies = Company.query.all()
        return render_template('select_company.html', companies=companies)

    except Exception as e:
        logging.error(f"Error in select_company route: {e}", exc_info=True)
        flash("An unexpected error occurred while selecting a company.", "error")
        return redirect(url_for('company_routes.select_company'))
