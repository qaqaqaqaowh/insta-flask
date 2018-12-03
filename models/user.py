from init import db, Model
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from helpers.validation import prepare_validation
from models.following import Following
from models.image import Image
import re


class User(Model, db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    is_private = db.Column(db.Boolean, default=False)
    is_valid = db.Column(db.Boolean, default=True)
    profile_img = db.Column(db.Text, nullable=False,
                            default='/static/download.png')
    images = relationship("Image", backref="user",
                          cascade="delete, delete-orphan")
    donations = relationship("Donation", backref="donor")
    followers = relationship(
        "User", secondary="followings", primaryjoin="and_(User.id==Following.user_id, Following.accepted==True)", secondaryjoin=id == db.foreign(Following.follower_id))
    following = relationship("User", secondary="followings",
                             primaryjoin="and_(User.id==Following.follower_id, Following.accepted==True)", secondaryjoin=id == db.foreign(Following.user_id))
    follower_requests = relationship(
        "User", secondary="followings", primaryjoin="and_(User.id==Following.user_id, Following.accepted==False)", secondaryjoin=id == db.foreign(Following.follower_id))

    feeds = relationship("Image", secondary="followings",
                         primaryjoin="and_(User.id==Following.follower_id, Following.accepted==True)", secondaryjoin="Image.user_id == Following.user_id", order_by="desc(Image.id)")

    def __init__(self, email, password, is_valid=None):
        if is_valid == None:
            self.is_valid = True
        self.email = email
        self.password = password

    @hybrid_property
    def logged_in(self):
        return self.is_authenticated

    @prepare_validation
    def change_password(self, old, new):
        if check_password_hash(self.password, old):
            self.password = new
        else:
            self.errors.append("Old Password is incorrect")
        return self

    @validates('email')
    @prepare_validation
    def email_validation(self, key, email):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            self.errors.append("Email format is incorrect")
        return email

    @validates('password')
    @prepare_validation
    def password_validation(self, key, password):
        if len(password) in range(8, 16):
            return generate_password_hash(password)
        else:
            self.errors.append("Password length should be between 8 - 15")

    def follow(self, user):
        follow = Following(user.id, self.id)
        if user.is_private:
            follow.accepted = False
        db.session.add(follow)
        db.session.commit()

    def unfollow(self, user):
        follow = Following.query.filter_by(
            user_id=user.id, follower_id=self.id).one()
        db.session.delete(follow)
        db.session.commit()
