"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy() 

default = 'https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png'


def connect_db(app):
    db.app = app 
    db.init_app(app) 

class Users(db.Model): 

    __tablename__ = 'users'

    @property
    def full_name(self):
        """ Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        p = self 
        return f"<User id={p.id} first name={p.first_name} last name={p.last_name}>"

    id = db.Column(db.Integer,
    primary_key=True,
    autoincrement=True) 

    first_name = db.Column(db.String(50),
    nullable=False) 

    last_name = db.Column(db.String(100),
    nullable=False) 

    image_url = db.Column(db.String(200), default = default) 

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')


class Post(db.Model): 
    """ Post for the blog """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    created_at = db.Column(
        db.DateTime,
        nullable=False, 
        default=datetime.datetime.now
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self): 
        """ a nicely-formatted date."""

        return self.created_at.strgtime("%a %b %-d %Y, %-I:%M %p")