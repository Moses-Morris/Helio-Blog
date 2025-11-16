#This is now a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


#database
db = SQLAlchemy()
DB_NAME = "database.db" 


def create_app():
    app = Flask(__name__)
    #app.config['secret_key'] = "30876adf7888fd2e3c50d787fa26d32b8cf488087502f85588f1ab84063cdc9a"   # This wont work since it is CASE SENSITIVE
    app.config['SECRET_KEY'] = "30876adf7888fd2e3c50d787fa26d32b8cf488087502f85588f1ab84063cdc9a"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #configure our database
    db.init_app(app) #initialize our db with our flask app
    #Get rid of this since you are going to use a blueprint for this
    #@app.route("/") 
    #def home():
        #return "<p>Hello People</p>"

    from .views import views 
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    #import database models
    from .models import User, Post, Comment, Like
    #call our database
    create_database(app)
    


    #setup login manager for session retain
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader   #This is a decorator to get the logged in user information #store the id in session
    def  load_user(id):
        return User.query.get(int(id))





    return app #this should be last in our funstion



#Database Function to create our database and run its functions
def create_database(app):
    if not path.exists("website/" + DB_NAME): #check if website and databse dont exist
        #db.create_all() #create if does not exist
        with app.app_context():
            db.create_all()
            print("Database created !!")
            print("Tables Created : ")
            print("1. User  !!")
            print("2. Post  !!")
            print("3. Comment  !!")
            print("4. Likes  !!")
