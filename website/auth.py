from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash



auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash(f"Welcome back, {user.username}!", category='success')
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password.", category='error')
        else:
            flash("Email not found. Please sign up.", category='error')

    return render_template("login.html", user=current_user)



#Registerr
@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("repeatpassword")
        print(username)
        
        #validate input before saving to database
        #validate Email
        check_email = User.query.filter_by(email=email).first()
        if check_email:
            flash("Email already registered. Use another email.", category='error')
            return  redirect(url_for('auth.signup'))
        if len(email) < 4:
            flash("Enter A Valid Email.", category='error')
            return  redirect(url_for('auth.signup'))

        #Validate Username
        check_username = User.query.filter_by(username=username).first()
        if check_username:
            flash("Username already registered. Use another username.", category='error')
            return  redirect(url_for('auth.signup'))
        if len(username) < 4:
            flash("Username is Short. \n Use more than 4 characters.", category='error')
            return  redirect(url_for('auth.signup'))
        
        #Validate Password
        if password != password2:
            flash("Passwords do not match", category='error')
            return  redirect(url_for('auth.signup'))
        if len(password) < 8:
            flash("Pasword is short. \n Should be more than 8 Characters. \n Include Alphanumeric Characters", category='error')
            return  redirect(url_for('auth.signup'))

        #Create User
        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        #OR you can login the user as you wish to handle the request
        #login_user(new_user, remember=True)
        flash(f"Signup Successful \n User Created {username}. \n Login to proceed.")
        return redirect(url_for('auth.login')) 

    return render_template("signup.html", user=current_user)



@login_required
@auth.route("/logout")
def logout():
    logout_user()
    print(f"Logged Out {current_user} successfuly")
    flash(f"Logout Successful \n ")
    return redirect(url_for("views.home"))