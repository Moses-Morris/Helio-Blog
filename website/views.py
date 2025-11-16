from flask import Blueprint, render_template, redirect, flash, request,url_for
from flask_login import login_required, current_user
views = Blueprint("views", __name__)

from .models import User, Post, Comment, Like
from . import db





@login_required
@views.route("/")
@views.route("/index")
@views.route("/home")
def home():
    #return "<h1>Home</h1>"
    if current_user.is_authenticated:
        print(current_user.username)

    #Get POSTS
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)





#View User Posts
@login_required
@views.route("/view/<id>", methods=['GET', 'POST'])
def view_posts(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post not Found", category='error')
        return redirect(url_for('views.home'))
    return render_template("view.html", user=current_user, post=post)





#View User Posts
@login_required
@views.route("/posts/<username>", methods=['GET', 'POST'])
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Username is invalid. \n View other user ", category='error')
        return redirect(url_for('views.home'))
    
    posts = Post.query.filter_by(author=user.id).all() #or posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)
    






#Create a Blog
@views.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    #return "<h1>Home</h1>"
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash("Post can not be empty", category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created Succesfully", category='success')


    return render_template("create_post.html", user=current_user)



#Delete a Blog
@login_required
@views.route("/delete/<id>", methods=['POST', 'GET'])
def delete(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post not Found", category='error')
    #Check if user owns the Post    
    elif current_user.id != post.author:
        flash("You can not delete this Post\n Login to Delete if you are the owner of the Post", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash(f"{post.text} Post successfully Deleted", category='success')
        print(f"{post.text} Post successfully Deleted")


    return redirect(url_for('views.home'))


 
#Comment on posts
#use the PostID for this
@login_required
@views.route("/comment/<id>", methods=['POST', 'GET'])
def comment(id):
    if id == " ":
        return redirect(url_for('views.home'))
    
    text = request.form.get('text')
    if not text:
        flash("Only text allowed. Can not be empty", category='error')
    else:
        post = Post.query.filter_by(id=id).first()
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment Added 🤖", category='success')
            print("Comment Added") 
        else:
            flash("There is no Post to Comment on" , category='error')
            return redirect(url_for('views.home'))

    return render_template("view.html", user=current_user, post=post)

#Delete Comments
@login_required
@views.route("/delete-comment/<id>", methods=['POST', 'GET'])
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if not comment:
        flash("Comment does not exist", category='error')
        return redirect(url_for('views.home'))
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You are not allowed to perform this action", category='error')
        return redirect(url_for('views.home'))
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Successfully Deleted the Comment", category='success')
    return redirect(url_for('views.home'))




#Likes of a Post
#Use post ID to add like
@login_required
@views.route("/like-add/<id>", methods=['POST', 'GET'])
def add_like(id):
    post = Post.query.filter_by(id=id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=id).first()

    if not post:
        flash("Post does not exist", category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=id)
        db.session.add(like)
        db.session.commit()
        #flash("Post Liked ", category='success')

    return redirect(url_for('views.home'))
   # elif like:
       # flash("Post does not have Action", category='error')
        #if like.types == 1:
            #flash("Post already Liked", category='success')
            #return redirect(url_for('views.home')) 
    #else:
       # one = 1
        #like = Like(author=current_user.id, post_id=post.id, types=one)
        #db.session.add(like)
        #db.session.commit()
        #flash("Post Liked ", category='success')