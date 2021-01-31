from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = '<f4b3a795f12ea88e7857c8f418c03ddcaaf3d60ebb6f76a3>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21022750:59djiCtLrWzzv7Z@csmysql.cs.cf.ac.uk:3306/c21022750_flasklabs'

db = SQLAlchemy(app)

from pennythoughts import routes



