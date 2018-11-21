from flask import Blueprint, redirect, request
from helpers.render import render
from models import user
from init import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

users_blueprint = Blueprint("users", __name__, template_folder="templates")

@users_blueprint.route("/new", methods=["GET"])
def new():
	return render("users/new.html")

@users_blueprint.route("/", methods=["POST"])
def create():
	return "Implementing"