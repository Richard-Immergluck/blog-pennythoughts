from datetime import datetime
from time import time
import re
from sqlalchemy.orm import backref
from pennythoughts import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# function to create urls for slugs
def slugify(s):
    RegEx = r'[^\w+]'
    return re.sub(RegEx, '-', s)

# Table for many to many relationship between posts and tags
posts_tags = db.Table('posts_tags',
                        db.Column('post_id', db.Integer, 
                        db.ForeignKey('post.id')),
                        db.Column('tag_id', db.Integer,
                        db.ForeignKey('tag.id'))
) 

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Dislikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Tag(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100))
        slug = db.Column(db.String(100), unique=True)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.slug = slugify(self.title)
        
        def __repr__(self):
            return f'<Tag id: {self.id}, title: {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post({self.post_id}'{self.date}', '{self.content}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slug = db.Column(db.String(150), unique=True)
    comments = db.relationship('Comment', backref='owner', lazy='dynamic')
    likes = db.relationship('Likes', backref='liked', lazy='dynamic')
    dislikes = db.relationship('Dislikes', backref='disliked', lazy='dynamic')
    tags = db.relationship('Tag', secondary=posts_tags, backref=db.backref('posts'), lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug
    
    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    first_name = db.Column(db.String(40), unique=True, nullable=False)
    last_name = db.Column(db.String(40), unique=True, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='owns', lazy=True)
    likes = db.relationship('Likes', backref='likes', lazy=True)
    dislikes = db.relationship('Dislikes', backref='dislikes', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = Likes(author_id=self.id, post_id=post.id)
            db.session.add(like)

    def dislike_post(self, post):
        if not self.has_disliked_post(post):
            dislike = Dislikes(author_id=self.id, post_id=post.id)
            db.session.add(dislike)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            Likes.query.filter_by(author_id=self.id, post_id=post.id).delete()
    
    def undislike_post(self, post):
        if self.has_disliked_post(post):
            Dislikes.query.filter_by(author_id=self.id, post_id=post.id).delete()

    def has_liked_post(self, post):
        return Likes.query.filter(Likes.author_id == self.id, Likes.post_id == post.id).count() > 0

    def has_disliked_post(self, post):
        return Dislikes.query.filter(Dislikes.author_id == self.id, Dislikes.post_id == post.id).count() > 0
    
    def avatar(self, size):
        avatar = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(avatar, size)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

