"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

@app.route('/users')
def list_users():
    """Shows list of all users in db"""

    users = User.query.all()
    return render_template('users/listing.html', users=users)

@app.route('/users/new', methods=["GET"])
def add_user_form():
    """Shows an add form for users"""

    return render_template('users/new_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Process the add form, adding a new user and going back to /users"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    flash(f"New user {new_user.full_name} created")

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Process the edit form, returning the user to the /users page"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"{user.full_name} details edited")

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted")

    return redirect("/users")


### *** PART 2 POSTS ROUTES *** ###


@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Show user's add post form"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Add post then redirect to user detail page"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"New Post: '{new_post.title}'!")

    return redirect(f"/users/{user.id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details about a single post"""

    post = Post.query.get_or_404(post_id)
    return render_template("posts/details.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show the edit page for a user's post"""

    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle the post edit form, returning the user to the /users page"""

    post = Post.query.get_or_404(post_id)
    post.title=request.form['title']
    post.content=request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a user's post"""
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted")

    return redirect(f"/users/{post.user_id}")


### *** PART 3 TAGS ROUTES *** ###


