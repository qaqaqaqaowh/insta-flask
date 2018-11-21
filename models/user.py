from init import db, Model
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates
from flask_login import UserMixin

class User(Model, db.Model, UserMixin):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.Text, unique=True)
	password = db.Column(db.Text)

	def __init__(self, email, password):
		self.email = email
		self.password = generate_password_hash(password)