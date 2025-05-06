import logging
from flask import Blueprint, jsonify, request, render_template
from datetime import datetime
from app import db
from app.models import PayrollRecord

payroll_routes = Blueprint('payroll_routes', __name__)

@payroll_routes.route('/add_payroll_form', methods=['GET'])
def add_payroll_form():
    """
    Render the form for adding a payroll record.
    """
    return render_template('add_payroll.html')

@payroll_routes.route('/add_payroll', methods=['POST'])
def add_payroll():
    try:
        data = request.form  # Accepting form data
        employee_name = data.get('employee_name')
        gross_wages = data.get('gross_wages')
        date_str = data.get('date')
        payg_withholding = data.get('payg_withholding', 0.0)
        superannuation = data.get('superannuation', 0.0)
        deductions = data.get('deductions', 0.0)
        company_id = data.get('company_id', 1)

        if not employee_name or not gross_wages or not date_str:
            logging.error(f"Invalid input data: {data}")
            return render_template('error.html', error_message="Employee name, gross wages, and date are required."), 400

        # Validate gross wages
        try:
            gross_wages = float(gross_wages)
        except ValueError:
            return render_template('error.html', error_message="Gross wages must be a positive number."), 400

        if gross_wages <= 0:
            return render_template('error.html', error_message="Gross wages must be greater than zero."), 400

        # Validate and parse date
        try:
            payroll_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return render_template('error.html', error_message="Invalid date format. Use YYYY-MM-DD."), 400

        # Calculate net pay
        net_pay = gross_wages - (float(payg_withholding) + float(deductions))

        # Create payroll record
        new_record = PayrollRecord(
            date=payroll_date,
            employee_name=employee_name,
            gross_wages=gross_wages,
            payg_withholding=float(payg_withholding),
            superannuation=float(superannuation),
            deductions=float(deductions),
            net_pay=net_pay,
            company_id=company_id
        )
        db.session.add(new_record)
        db.session.commit()

        logging.info(f"Payroll record added for {employee_name}.")
        return render_template('success.html', message="Payroll record added successfully!")

    except Exception as e:
        logging.error(f"Error adding payroll record: {str(e)}", exc_info=True)
        return render_template('error.html', error_message=f"Failed to add payroll record: {str(e)}"), 500

@payroll_routes.route('/view_payroll_records', methods=['GET'])
def view_payroll_records():
    try:
        payroll_records = PayrollRecord.query.all()
        if not payroll_records:
            logging.info("No payroll records found.")
            return render_template('view_payroll_records.html', payroll_records=[])

        records = [
            {
                "id": record.id,
                "date": record.date.strftime('%Y-%m-%d') if record.date else None,
                "employee_name": record.employee_name,
                "gross_wages": record.gross_wages,
                "payg_withholding": record.payg_withholding,
                "superannuation": record.superannuation,
                "deductions": record.deductions,
                "net_pay": record.net_pay,
                "company_id": record.company_id
            }
            for record in payroll_records
        ]

        logging.info(f"Fetched {len(records)} payroll records successfully.")
        return render_template('view_payroll_records.html', payroll_records=records)

    except Exception as e:
        logging.error(f"Error fetching payroll records: {str(e)}", exc_info=True)
        return render_template('error.html', error_message=f"Failed to fetch payroll records: {str(e)}"), 500

@payroll_routes.route('/payslip/<int:record_id>', methods=['GET'])
def generate_payslip(record_id):
    try:
        record = PayrollRecord.query.get(record_id)
        if not record:
            return render_template('error.html', error_message="Payslip not found"), 404

        return render_template(
            'payslip.html',
            employee_name=record.employee_name,
            payroll_date=record.date.strftime('%Y-%m-%d'),
            gross_wages=record.gross_wages,
            payg_withholding=record.payg_withholding,
            superannuation=record.superannuation,
            deductions=record.deductions,
            net_pay=record.net_pay
        )
    except Exception as e:
        logging.error(f"Error generating payslip: {e}", exc_info=True)
        return render_template('error.html', error_message="Failed to generate payslip"), 500
