from flask import Blueprint, redirect, request, url_for, flash
from flask_login import login_required, current_user
from models import User, Following
from init import db

followings_blueprint = Blueprint(
    "followings", __name__, template_folder="templates")


@followings_blueprint.route('/<id>', methods=["POST"])
@login_required
def follow(id):
    user = User.query.get(id)
    if not current_user in user.follower_requests:
        current_user.follow(user)
        if user.is_private:
            flash("Request sent!")
        else:
            flash("Followed User!")
    else:
        flash("Please wait for request to be confirmed")
    return redirect(url_for('users.show', id=user.id), code=200)


@followings_blueprint.route('/<id>/accept', methods=["POST"])
@login_required
def accept(id):
    follow = Following.query.filter_by(
        user_id=current_user.id, follower_id=id).one()
    follow.accepted = True
    db.session.add(follow)
    db.session.commit()
    return redirect(url_for('users.show', id=current_user.id), code=200)


@followings_blueprint.route('/<id>/decline', methods=["POST"])
@login_required
def decline(id):
    follower = User.query.get(id)
    follower.unfollow(current_user)
    return redirect(url_for('users.show', id=current_user.id), code=200)
