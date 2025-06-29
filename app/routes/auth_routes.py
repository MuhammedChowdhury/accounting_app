from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, UserMixin
from app.models import User as DBUser, db

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = DBUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))

        flash("Invalid credentials.")
        return redirect(url_for("auth_routes.login"))

    return render_template("login.html")


@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = DBUser.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("auth_routes.register"))

        user = DBUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("home"))

    return render_template("register.html")

@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_routes.login"))