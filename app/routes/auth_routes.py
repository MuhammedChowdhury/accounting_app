from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, UserMixin

auth_routes = Blueprint("auth_routes", __name__)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password123":
            user = User(id=username)
            login_user(user)
            return redirect(url_for("home"))

        return "Invalid credentials", 401

    return render_template("login.html")

@auth_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))