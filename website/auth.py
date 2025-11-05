from flask import Blueprint

auth = Blueprint("auth", __main__)


@auth.route("/")
def login():
    return "Login"