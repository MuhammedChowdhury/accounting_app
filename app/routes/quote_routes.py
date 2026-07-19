import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from app.models import Company, Quote

quote_routes = Blueprint('quote_routes', __name__)

@quote_routes.route('/add_quote', methods=['GET', 'POST'])
def add_quote():
    """Renders the quote generator or saves a new estimate record row."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        if not company_id:
            return redirect(url_for('company_routes.select_company'))
        company = db.session.get(Company, company_id)

        if request.method == 'POST':
            customer_name = request.form.get('customer_name')
            line_items = request.form.get('line_items')
            total_amount = request.form.get('total_amount', type=float, default=0.0)
            validity_str = request.form.get('validity_period')

            if customer_name and total_amount:
                from datetime import datetime
                try:
                    validity_period = datetime.strptime(validity_str, '%Y-%m-%d').date()
                except Exception:
                    validity_period = datetime.utcnow().date()

                new_quote = Quote(
                    customer_name=customer_name,
                    line_items=line_items,
                    total_amount=total_amount,
                    validity_period=validity_period
                )
                db.session.add(new_quote)
                db.session.commit()
                return redirect(url_for('quote_routes.view_quotes', company_id=company_id))

        return render_template('add_quote.html', company=company)
    except Exception as e:
        logging.error(f"Quote generation route crash: {e}", exc_info=True)
        return jsonify({'error': 'Configuration failure.'}), 500

@quote_routes.route('/view_quotes', methods=['GET'])
def view_quotes():
    """Fetches every cost estimate log registered inside database."""
    try:
        company_id = request.args.get('company_id', type=int) or session.get('company_id')
        company = db.session.get(Company, company_id)
        quotes = db.session.query(Quote).all()
        return render_template('view_quotes.html', company=company, quotes=quotes)
    except Exception as e:
        logging.error(f"Quotes registry log rendering failure: {e}", exc_info=True)
        return jsonify({'error': 'Database extraction failed.'}), 500
