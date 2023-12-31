from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

# First, create a ***User*** model for SQLAlchemy. Put this in a ***models.py*** file.

# It should have the following columns:

# - ***id***, an autoincrementing integer number that is the primary key
# - ***first_name*** and ***last_name***
# - ***image_url*** for profile images

# Make good choices about whether things should be required, have defaults, and so on.

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                          nullable=False,
                          unique=True)
    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=True)
    image_url = db.Column(db.String(500),
                          nullable=False,
                          unique=False,
                          default=None)
    
    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(500),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user_name = db.relationship('User', backref='posts')
    tags = db.relationship('PostTag', back_populates='post', lazy='dynamic')

    def __repr__(self):
        return f"<id={self.id} title={self.title} content={self.content} tags={self.tags} user_name={self.user_name}>"
               
class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     unique=True)
    
    posts = db.relationship('PostTag', back_populates='tag', lazy='dynamic')
    
class PostTag(db.Model):

    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), 
                        primary_key=True, nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), 
                       primary_key=True, nullable=False)
    
    post = db.relationship('Post', back_populates='tags', lazy='joined')
    tag = db.relationship('Tag', back_populates='posts', lazy='joined')