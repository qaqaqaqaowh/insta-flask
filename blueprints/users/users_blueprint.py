from flask import Blueprint, redirect
from helpers.render import render

users_blueprint = Blueprint("users", __name__, template_folder="templates/users")

@users_blueprint.route("/new", methods=["GET"])
def new():
	return render("new.html")

@users_blueprint.route("/", methods=["POST"])
def create():
	return "Implementing"