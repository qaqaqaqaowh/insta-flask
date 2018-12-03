from flask import Blueprint, redirect, request, url_for, flash
from flask_login import login_required, current_user
from helpers.render import render
from models.user import User
from init import login_manager, db
from wtforms import StringField, PasswordField, BooleanField, FileField
from flask_wtf import FlaskForm
from helpers.csrf import csrf_validate
from helpers.image_uploader import upload_image


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


@users_blueprint.route("/<id>", methods=["GET"])
def show(id):
    user = User.query.get(id)
    if user:
        return render("users/show.html", user=user)
    else:
        return render("404.html")


@users_blueprint.route("/edit", methods=["GET"])
def edit():
    if not current_user.is_valid:
        return redirect(url_for("sessions.oauth_cleanup"))
    form = EditForm()
    form.is_private.data = current_user.is_private
    return render("users/edit.html", form=form)


@users_blueprint.route("/update", methods=["POST"])
def update():
    if request.form.get("_method") == "PUT":
        form = EditForm()
        image = form.image.data
        if image:
            current_user.profile_img = upload_image(image)
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
