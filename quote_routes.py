from flask import Blueprint, request, jsonify, render_template
from app.models import db, Quote
from datetime import datetime

quote_routes = Blueprint('quote_routes', __name__)

### 🔹 Add a Quote ###
@quote_routes.route('/add_quote', methods=['POST'])
def add_quote():
    """Receives quote data and saves it to the database."""
    try:
        data = request.form
        customer_name = data.get('customer_name')
        line_items = data.get('line_items')
        total_amount = float(data.get('total_amount'))
        validity_period = datetime.strptime(data.get('validity_period'), '%Y-%m-%d')

        if not customer_name or not line_items or not total_amount or not validity_period:
            return jsonify({'error': 'Missing required fields'}), 400

        new_quote = Quote(
            customer_name=customer_name,
            line_items=line_items,
            total_amount=total_amount,
            validity_period=validity_period,
            payment_status="Pending"  # Default status
        )
        db.session.add(new_quote)
        db.session.commit()

        return jsonify({'message': '✅ Quote added successfully!', 'quote_id': new_quote.id}), 201
    except ValueError as ve:
        return jsonify({'error': f'⚠ Invalid data type: {str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to add quote: {str(e)}'}), 500

### 🔹 View Quotes (HTML) ###
@quote_routes.route('/view_quotes', methods=['GET'])
def view_quotes():
    """Displays quotes in an HTML template."""
    try:
        quotes = Quote.query.all()
        return render_template('quotes.html', quotes=quotes)
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to fetch quotes: {str(e)}'}), 500

### 🔹 View Quotes (JSON) ###
@quote_routes.route('/api/quotes', methods=['GET'])
def get_quotes():
    """Returns all quotes in JSON format."""
    try:
        quotes = Quote.query.all()
        return jsonify([{
            'id': quote.id,
            'customer_name': quote.customer_name,
            'line_items': quote.line_items,
            'total_amount': quote.total_amount,
            'validity_period': quote.validity_period.strftime('%Y-%m-%d'),
            'payment_status': quote.payment_status
        } for quote in quotes]), 200
    except Exception as e:
        return jsonify({'error': f'⚠ Failed to fetch quotes: {str(e)}'}), 500
