import os
from flask import Blueprint, redirect, request, url_for, flash
from helpers.render import render
from models.user import User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from helpers.csrf import csrf_validate
from init import oauth, db

sessions_blueprint = Blueprint(
    "sessions", __name__, template_folder="templates")


class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")


class ResetForm(FlaskForm):
    password = PasswordField("Password")
    password_conf = PasswordField("Confirm Password")


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


@sessions_blueprint.route("/google", methods=["GET"])
def google():
    redirect_url = url_for('sessions.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_url)


@sessions_blueprint.route("/google/callback", methods=["GET"])
def google_callback():
    oauth.google.authorize_access_token()
    resp = oauth.google.get(
        'https://www.googleapis.com/oauth2/v2/userinfo').json()["email"]
    user = User.query.filter_by(email=resp).one_or_none()
    if user:
        if user.is_valid:
            login_user(user)
            return redirect(url_for("index"), code=200)
        else:
            return redirect(url_for("sessions.oauth_cleanup"), code=200)
    else:
        user = User(resp, "12345678", is_valid=False)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=resp).one_or_none()
        login_user(user)
        return redirect(url_for("sessions.oauth_cleanup"), code=200)


@sessions_blueprint.route("/oauth/cleanup", methods=["GET"])
def oauth_cleanup():
    if not current_user.is_valid:
        form = ResetForm()
        return render("sessions/oauth_cleanup.html", form=form)
    else:
        return render("404.html")


@sessions_blueprint.route("/oauth/cleanup", methods=["POST"])
def oauth_cleanup_post():
    form = ResetForm()
    if not current_user.is_valid and csrf_validate(form) and form.password.data == form.password_conf.data:
        current_user.password = form.password.data
        current_user.is_valid = True
        db.session.add(current_user)
        db.session.commit()
        flash("Setting successful!")
    else:
        flash("Password setting failed, edit user to try again!")
    return redirect(url_for("users.show", id=current_user.id))
