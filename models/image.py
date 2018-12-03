from init import db, Model
from sqlalchemy.orm import relationship


class Image(Model, db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    caption = db.Column(db.Text)
    donations = relationship("Donation", backref="image")

    def __init__(self, url, caption):
        self.url = url
        self.caption = caption
