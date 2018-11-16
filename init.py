import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
######################################
#### SET UP OUR SQLite DATABASE #####
####################################
# Instead of hard coding our current project's working directory, this line of code grabs our directory path correctly regardless of our operating system
basedir = os.path.abspath(os.path.dirname(__file__))
# Try to understand this by printing out what basedir is
# print(basedir)

app = Flask(__name__)
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Model:
	def __repr__(self):
		string = f"<{type(self).__name__}"
		for index, pair in enumerate(self.__dict__.items()):
			if index == 0: continue
			string += f", {pair[0]}: {pair[1]}"
		string += ">"
		return string

# Add on migration capabilities in order to run terminal commands
Migrate(app,db)