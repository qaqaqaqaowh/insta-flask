from init import db
from flask import Blueprint, redirect, request, url_for, flash
from helpers.render import render
from flask_login import login_required, current_user
from helpers.csrf import csrf_validate
from helpers.payment import bt_pay
from models.donation import Donation
from models.image import Image

donations_blueprint = Blueprint(
    "donations", __name__, template_folder="templates")


@donations_blueprint.route("/images/<img_id>", methods=["POST"])
@login_required
def create(img_id):
    image = Image.query.get(img_id)
    if not image.user == current_user:
        amount = request.form.get("amount")
        nonce = request.form.get("bt-nonce")
        result = bt_pay(nonce, amount)
        if result.is_success:
            donation = Donation(current_user.id, image.id, amount)
            db.session.add(donation)
            db.session.commit()
            flash("Donation Successful!")
        else:
            flash("Payment went wrong!")
    else:
        flash("Can't donate to self!")
    return redirect(url_for("images.show", id=image.id))
