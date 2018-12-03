from init import db
from flask import Blueprint, redirect, request, url_for, flash
from helpers.render import render
from flask_login import login_required, current_user
from helpers.csrf import csrf_validate
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from models.image import Image
from helpers.image_uploader import upload_image
from helpers.payment import gateway

images_blueprint = Blueprint(
    "images", __name__, template_folder="templates")


class CreateImageForm(FlaskForm):
    image = FileField("Image")
    caption = StringField("Caption")


@images_blueprint.route("/new", methods=["GET"])
@login_required
def new():
    form = CreateImageForm()
    return render("images/new.html", form=form)


@images_blueprint.route("/", methods=["POST"])
@login_required
def create():
    form = CreateImageForm()
    if csrf_validate(form):
        url = upload_image(form.image.data)
        image = Image(url, form.caption.data)
        current_user.images.append(image)
        db.session.add(image)
        db.session.commit()
        flash("Image upload Success")
        return redirect(url_for("users.show", id=current_user.id), code=200)
    else:
        flash("Nope")
        return render("images/new.html", form=form)


@images_blueprint.route("/<id>", methods=["GET"])
def show(id):
    image = Image.query.get(id)
    token = gateway.client_token.generate()
    if image:
        return render("images/show.html", image=image, token=token)
    return render("404.html")
