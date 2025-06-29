from flask import Blueprint, request, jsonify

subscribe_routes = Blueprint("subscribe_routes", __name__)

@subscribe_routes.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email")
    if email:
        # Save to database (optional)
        return jsonify({"message": f"Thanks for subscribing, {email}!"})
    return jsonify({"error": "Email is required!"}), 400
