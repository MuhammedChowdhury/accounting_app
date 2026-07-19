import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, Employee, PayrollRun

payroll_routes = Blueprint('payroll_routes', __name__)

@payroll_routes.route('/payroll', methods=['GET', 'POST'])
def payroll_dashboard():
    """Manages firm payroll cycles, active employee listings, and STP calculations."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))

        company = db.session.get(Company, company_id)
        if not company:
            return redirect(url_for('company_routes.select_company'))

        session['company_id'] = company.id

        if request.method == 'POST':
            # Run payroll row execution calculations
            employee_id = request.form.get('employee_id', type=int)
            start_date = request.form.get('pay_period_start')
            end_date = request.form.get('pay_period_end')
            gross_wages = request.form.get('gross_wages', type=float, default=0.0)

            if not employee_id or not start_date or not end_date:
                return jsonify({'error': 'Missing mandatory calculation values.'}), 400

            super_guarantee = round(gross_wages * 0.12, 2)
            payg_withholding = round(gross_wages * 0.15, 2)
            net_pay = round(gross_wages - payg_withholding, 2)

            new_run = PayrollRun(
                employee_id=employee_id,
                pay_period_start=start_date,
                pay_period_end=end_date,
                gross_wages=gross_wages,
                payg_withholding=payg_withholding,
                super_guarantee=super_guarantee,
                net_pay=net_pay,
                stp_status="Pending Submission"
            )
            db.session.add(new_run)
            db.session.commit()
            return redirect(url_for('payroll_routes.payroll_dashboard', company_id=company_id))

        employees = db.session.query(Employee).all()
        payroll_history = db.session.query(PayrollRun).all()

        return render_template(
            'payroll.html',
            company=company,
            employees=employees,
            payroll_history=payroll_history
        )
    except Exception as e:
        logging.error(f"Payroll rendering error: {e}", exc_info=True)
        return jsonify({'error': 'Initialization failed.'}), 500


@payroll_routes.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    """⚠️ NEW SEPARATE LINK PATH: Adds fresh staff profiles into the firm database."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        company = db.session.get(Company, company_id)

        if request.method == 'POST':
            name = request.form.get('name')
            tfn = request.form.get('tfn')
            emp_type = request.form.get('employment_type', 'Full-Time')
            tfn_status = request.form.get('tfn_declaration_status', 'Submitted')

            if name:
                new_staff = Employee(
                    name=name,
                    tfn=tfn,
                    employment_type=emp_type,
                    tfn_declaration_status=tfn_status
                )
                db.session.add(new_staff)
                db.session.commit()
            return redirect(url_for('payroll_routes.payroll_dashboard', company_id=company_id))

        return render_template('add_employee.html', company=company)
    except Exception as e:
        logging.error(f"Error adding worker rows: {e}", exc_info=True)
        return jsonify({'error': 'Could not save profile.'}), 500
