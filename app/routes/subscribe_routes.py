import logging
from flask import Blueprint, request, jsonify, flash, redirect, url_for
from app.models import db, Subscriber

subscribe_routes = Blueprint("subscribe_routes", __name__)

@subscribe_routes.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.json.get("email") if request.is_json else request.form.get("email")

        if not email or not email.strip():
            return jsonify({"error": "Email identifier is mandatory."}), 400

        email = email.strip().lower()
        existing_sub = db.session.query(Subscriber).filter_by(email=email).first()
        if existing_sub:
            return jsonify({"message": f"Thanks for subscribing, {email}! (Account already registered)"}), 200

        new_subscriber = Subscriber(email=email)
        db.session.query(Subscriber).session.add(new_subscriber)
        db.session.commit()

        return jsonify({"message": f"Thanks for subscribing, {email}!"}), 201
    except Exception as e:
        logging.error(f"Subscription database write loop anomaly tracking: {e}", exc_info=True)
        return jsonify({"error": "Internal database tracking logging failure."}), 500
