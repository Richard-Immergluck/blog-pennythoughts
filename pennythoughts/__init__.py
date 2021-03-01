from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_mail import Mail

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = '<f4b3a795f12ea88e7857c8f418c03ddcaaf3d60ebb6f76a3>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21022750:59djiCtLrWzzv7Z@csmysql.cs.cf.ac.uk:3306/c21022750_pennythoughts_db'

# DB object that represents the database

db = SQLAlchemy(app)

# Object for Migration Engine
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)

# For Moment date/time functions
moment = Moment(app)

from pennythoughts import routes, models

from flask_admin import Admin
from pennythoughts.views import AdminView
from pennythoughts.models import User, Post, Comment, Tag
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))
admin.add_view(AdminView(Tag, db.session))


# Flask Mail Extension config

mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'rimmergluck@googlemail.com'
app.config["MAIL_PASSWORD"] = 'Em1lyjane'

mail.init_app(app)
