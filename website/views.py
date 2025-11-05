from flask import Blueprint, render_template, redirect

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/index")
@views.route("/home")
def home():
    #return "<h1>Home</h1>"
    return render_template("home.html", name="Moses")