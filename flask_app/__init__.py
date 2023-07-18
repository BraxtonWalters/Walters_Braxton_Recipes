import re
from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "shhhhhh"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$') 
bcrypt = Bcrypt(app)
#! add the database!!!
DATABASE = "recipes"


# pipenv install flask pymysql flask-bcrypt
# pipenv shell
# python server.py