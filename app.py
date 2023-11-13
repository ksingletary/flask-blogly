"""Blogly application."""

from flask import Flask, redirect, render_template, flash, session, request
from models import db, connect_db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'gfgfgfggg'

connect_db(app)
db.create_all()

@app.route('/')
def user_page():
    """Displays Users for now"""

    users = User.query.all()
    return render_template('user_page.html', users=users)

@app.route('/add_user')
def user_form():
    """Displays New User Form"""
    return render_template("add_user.html")


@app.route('/', methods=["POST"])
def create_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form.get("img_url")

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/{new_user.id}")

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single pet"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    
    return render_template("details.html", user=user, posts=posts)

@app.route('/<int:user_id>/edit_user')
def show_edit_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)

@app.route('/<int:user_id>/edit_user', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form.get("img_url")

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()

    return redirect("/") 

@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()

    db.session.commit()
    return redirect("/")

@app.route('/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    

    return render_template('new_post.html', user=user)

@app.route('/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    
    title = request.form.get("title")
    content = request.form.get("content")

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    
    return render_template('edit_post.html', post=post) 

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form.get("title")
    content = request.form.get("content")

    post.title = title
    post.content = content
    db.session.commit()
    
    return redirect(f"/posts/{post_id}") 

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()
    return redirect("/")



