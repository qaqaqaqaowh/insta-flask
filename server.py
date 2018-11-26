from flask import Flask, redirect, request as req
from init import app, db
from blueprints import sessions_blueprint, users_blueprint

from helpers.render import render

app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(users_blueprint, url_prefix="/users")


@app.route("/", methods=["GET"])
def index():
    return render("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
