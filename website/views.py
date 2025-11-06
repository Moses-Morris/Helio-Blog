from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
views = Blueprint("views", __name__)

@login_required
@views.route("/")
@views.route("/index")
@views.route("/home")
def home():
    #return "<h1>Home</h1>"
    if current_user.is_authenticated:
        print(current_user.username)
    return render_template("home.html", user=current_user)



#Create a Blog
@login_required
@views.route("/create", methods=['GET', 'POST'])
def create():
    #return "<h1>Home</h1>"
    return render_template("create_post.html", user=current_user)