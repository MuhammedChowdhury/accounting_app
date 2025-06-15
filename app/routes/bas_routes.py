import logging
from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import func
from datetime import datetime
from app.models import FinancialRecord, PayrollRecord, Company
from app import db

# Create a Blueprint for BAS-related routes
bas_routes = Blueprint('bas_routes', __name__)

@bas_routes.route('/bas_form', methods=['GET'])
def bas_form():
    """
    Renders the BAS Report Form for user input.
    """
    return render_template('bas_report_form.html')


@bas_routes.route('/bas_result', methods=['POST'])
def bas_report():
    """
    Generates a BAS report with GST, PAYG Withholding, PAYG Instalments, and Summary details.
    """
    try:
        # Retrieve query parameters
        company_name = request.args.get('company_name')
        company_id = request.args.get('company_id', type=int)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        instalment_rate = request.args.get('instalment_rate', 0.10, type=float)

        # Validate company details
        if company_name:
            company = Company.query.filter_by(name=company_name).first()
            if not company:
                return jsonify({"error": f"Company with name '{company_name}' not found."}), 404
            company_id = company.id
        elif not company_id:
            return jsonify({"error": "Please provide a company_name or company_id."}), 400

        # Validate date range
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
            date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None
        except ValueError:
          return jsonify({"error": "Invalid date format. Use DD-MM-YYYY."}), 400

        # Return the rendered HTML with the report data
        return render_template("bas_result.html", report=response)    


        # GST Fields
        gst_query = db.session.query(FinancialRecord).filter(FinancialRecord.company_id == company_id)
        if date_from and date_to:
            gst_query = gst_query.filter(FinancialRecord.date >= date_from, FinancialRecord.date <= date_to)

        total_sales = gst_query.filter(FinancialRecord.type_of_income == "sales").with_entities(func.sum(FinancialRecord.credit)).scalar() or 0.0
        export_sales = gst_query.filter(FinancialRecord.type_of_income == "export").with_entities(func.sum(FinancialRecord.credit)).scalar() or 0.0
        gst_free_sales = gst_query.filter(FinancialRecord.type_of_income == "gst_free").with_entities(func.sum(FinancialRecord.credit)).scalar() or 0.0
        gst_on_sales = db.session.query(func.sum(FinancialRecord.gst_received)).filter(FinancialRecord.company_id == company_id).scalar() or 0.0
        gst_on_purchases = db.session.query(func.sum(FinancialRecord.gst_paid)).filter(FinancialRecord.company_id == company_id).scalar() or 0.0

        # PAYG Withholding Fields
        total_wages = db.session.query(func.sum(PayrollRecord.gross_wages)).filter(PayrollRecord.company_id == company_id).scalar() or 0.0
        payg_withholding = db.session.query(func.sum(PayrollRecord.payg_withholding)).filter(PayrollRecord.company_id == company_id).scalar() or 0.0
        other_withheld = db.session.query(func.sum(PayrollRecord.deductions)).filter(PayrollRecord.company_id == company_id).scalar() or 0.0

        # PAYG Instalments
        payg_income = db.session.query(func.sum(FinancialRecord.credit)).filter(
            FinancialRecord.company_id == company_id,
            FinancialRecord.type_of_income == "payg_income"
        ).scalar() or 0.0
        instalment_amount = payg_income * instalment_rate

        # Summary
        gst_payable = gst_on_sales - gst_on_purchases
        total_withheld = payg_withholding + other_withheld
        net_payable = gst_payable + total_withheld + instalment_amount

        # Response structure
        response = {
            "metadata": {
                "company_name": company.name if company_name else f"Company ID {company_id}",
                "reporting_period": {
                    "from": date_from.strftime('%Y-%m-%d') if date_from else "Not provided",
                    "to": date_to.strftime('%Y-%m-%d') if date_to else "Not provided",
                }
            },
            "GST": {
                "G1_Total_Sales": total_sales,
                "G2_Export_Sales": export_sales,
                "G3_Other_GST_Free_Sales": gst_free_sales,
                "1A_GST_on_Sales": gst_on_sales,
                "1B_GST_on_Purchases": gst_on_purchases
            },
            "PAYG_Withholding": {
                "W1_Total_Wages": total_wages,
                "W2_PAYG_Withholding": payg_withholding
            },
            "PAYG_Instalments": {
                "T1_PAYG_Income": payg_income,
                "T11_Instalment_Amount": instalment_amount
            },
            "Summary": {
                "GST_Payable": gst_payable,
                "PAYG_Withholding": total_withheld,
                "Net_Amount_Payable": net_payable
            }
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error generating BAS report: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate BAS report"}), 500
