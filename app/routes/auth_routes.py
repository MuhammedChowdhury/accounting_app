import logging
from flask import Blueprint, request, redirect, url_for, render_template, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    """Handles secure workspace user authentication sessions."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            # Sends you directly onto your fixed central landing hub page
            return redirect(url_for("index"))

        flash("Invalid credentials.")
        return redirect(url_for("auth_routes.login"))

    return render_template("login.html")


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    """Smart Gate: Open if database is empty, strictly locked to Admins if profiles exist."""
    try:
        # Count the number of total users registered in the system
        total_users = db.session.query(User).count()
        
        # Security Gate: If profiles exist, ensure the visitor is an authenticated Admin
        if total_users > 0:
            if not current_user.is_authenticated or getattr(current_user, 'role', None) != 'Admin':
                logging.warning(f"Blocked unauthorized registration from: {getattr(current_user, 'username', 'Anonymous')}")
                return jsonify({'error': 'Access Denied: Only a Firm Administrator can register new profiles.'}), 403

    except Exception as e:
        logging.error(f"Database connectivity check failed inside registration gate: {e}")
        return jsonify({'error': 'Internal system configuration connectivity error.'}), 500

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "Bookkeeper")

        if not username or not password:
            flash("Username and password fields are required.")
            return render_template("register.html", initial_setup=(total_users == 0))

        # Verify that the username doesn't already exist inside the columns
        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            flash("Username profile already exists inside system registry.")
            return render_template("register.html", initial_setup=(total_users == 0))

        # Force Override: The very first user to sign up MUST be an Admin
        final_role = "Admin" if total_users == 0 else role

        # Build and commit the new profile safely into local database tables
        new_user = User(username=username, role=final_role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Successfully registered account {username} as {final_role}.")
        
        # If this was the first setup, log them in automatically to prevent roadblock loops
        if total_users == 0:
            login_user(new_user)
            return redirect(url_for("index"))
            
        return redirect(url_for("index"))

    return render_template("register.html", initial_setup=(total_users == 0))


@auth_routes.route("/logout")
@login_required
def logout():
    """De-authenticates active system session tokens and clears corporate memory loops."""
    logout_user()
    if 'company_id' in session:
        session.pop('company_id')
    return redirect(url_for("auth_routes.login"))
