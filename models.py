from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.String(255),
                          nullable=False,
                          unique=True,
                          default=None)
    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name
    
                        
