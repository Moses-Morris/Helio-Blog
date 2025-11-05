#This is now a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['secret_key'] = "blogdaily"
    
    #Get rid of this since you are going to use a blueprint for this
    #@app.route("/") 
    #def home():
        #return "<p>Hello People</p>"

    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")


    return app