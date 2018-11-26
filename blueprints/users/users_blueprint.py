from flask import Blueprint, redirect, request, url_for, flash
from flask_login import login_required, current_user
from helpers.render import render
from models.user import User
from init import login_manager, db
from wtforms import StringField, PasswordField, BooleanField, FileField
from flask_wtf import FlaskForm
from helpers.csrf import csrf_validate
from google.cloud import storage
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


users_blueprint = Blueprint("users", __name__, template_folder="templates")


class RegistrationForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")


class EditForm(FlaskForm):
    image = FileField('Profile Image')
    is_private = BooleanField("Private?")
    old_password = PasswordField("Old Password")
    password = PasswordField("Password")
    password_conf = PasswordField("Password Confirmation")


@users_blueprint.route("/new", methods=["GET"])
def new():
    return render("users/new.html", form=RegistrationForm())


@users_blueprint.route("/", methods=["POST"])
def create():
    form = RegistrationForm(request.form)
    user = User(form.email.data, form.password.data)
    if not user.errors and csrf_validate(form):
        db.session.add(user)
        db.session.commit()
        flash("Done, Login now!")
        return redirect(url_for('sessions.new'), code=200)
    else:
        flash(', '.join(user.errors))
        return render("users/new.html", form=form)


@users_blueprint.route("/users/<id>", methods=["GET"])
def show(id):
    user = User.query.get(id)
    if user and (not user.is_private or current_user.id == user.id):
        return render("users/show.html", user=user)
    else:
        return render("404.html")


@users_blueprint.route("/user/edit", methods=["GET"])
def edit():
    form = EditForm()
    form.is_private.data = current_user.is_private
    return render("users/edit.html", form=form)


@users_blueprint.route("/users/update", methods=["POST"])
def update():
    if request.form.get("_method") == "PUT":
        form = EditForm()
        image = form.image.data
        if image:
            gcs = storage.Client()
            bucket = gcs.get_bucket(os.environ.get("GCS_BUCKET"))
            blob = bucket.blob(image.filename)
            blob.upload_from_string(
                image.read(),
                content_type=image.content_type
            )
            current_user.profile_img = blob.public_url
        if form.password.data == form.password_conf.data:
            current_user.is_private = form.is_private.data
            current_user.change_password(
                form.old_password.data, form.password.data)
            if not current_user.errors:
                db.session.add(current_user)
                db.session.commit()
                flash("Updated!")
                return redirect(url_for("users.show", id=current_user.id), code=200)
            else:
                flash(",".join(current_user.errors))
        else:
            flash("New and old password doesn't match")
        return render("users/edit.html", form=form)
