from flask import Blueprint, redirect, request, url_for, flash
from helpers.render import render
from models.user import User
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from helpers.csrf import csrf_validate

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")


@sessions_blueprint.route("/new", methods=["GET"])
def new():
    return render("sessions/new.html", form=LoginForm())


@sessions_blueprint.route("/", methods=["POST"])
def create():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).one_or_none()
    if user and check_password_hash(user.password, form.password.data) and csrf_validate(form):
        login_user(user)
        flash("Done Logging in!")
        return redirect(url_for("index"), code=200)
    else:
        flash("Bad Login")
        return render("sessions/new.html", form=form)


@sessions_blueprint.route("/logout", methods=["POST"])
def destroy():
    print(request.form.get("_method") == "DELETE")
    if request.form.get("_method") == "DELETE":
        logout_user()
        flash("Logged Out!")
        return redirect(url_for('index'), code=200)
