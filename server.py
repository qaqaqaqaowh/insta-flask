from flask import Flask, redirect, request as req
from flask_login import current_user
from init import app, db
from blueprints import *

from helpers.render import render

app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followings_blueprint, url_prefix="/following")


@app.route("/", methods=["GET"])
def index():
    return render("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
