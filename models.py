from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

"""Models for Blogly."""

class User(db.Model):
    """Blog Users Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    
    first_name = db.Column(db.String(50),
                     nullable=False)
    
    last_name = db.Column(db.String(50),
                     nullable=False)
    
    image_url = db.Column(db.Text, 
                     nullable=False,
                     default=DEFAULT_IMAGE_URL)
    
    # image_url = db.Column(db.String(50),
    #                  nullable=False,
    #                  unique=True)
    
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Blog Posts Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)

    title = db.Column(db.Text, 
                      nullable=False)

    content = db.Column(db.Text, 
                        nullable=False)

    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.datetime.now)

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False,)
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        return f"<Employee {self.title} {self.scontent} {self.created_at} {self.user_id} >"


class Tag(db.Model):
    """Tags Model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    name = db.Column(db.Text, 
                     nullable=False, 
                     unique=True)

    

class PostTag(db.Model):
    """Tags on a Post Model"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key=True)

    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True)
