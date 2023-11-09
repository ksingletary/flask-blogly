"""Blogly application."""

from flask import Flask, redirect, render_template, flash, session, request
from models import db, connect_db, User


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
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/{new_user.id}")

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)



