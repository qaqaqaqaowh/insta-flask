from flask import Blueprint, redirect
from helpers.render import render

sessions_blueprint = Blueprint("sessions", __name__, template_folder="templates/sessions")

@sessions_blueprint.route("/new", methods=["GET"])
def new():
	return render("new.html")

@sessions_blueprint.route("/", methods=["POST"])
def create():
	return "Implementing"