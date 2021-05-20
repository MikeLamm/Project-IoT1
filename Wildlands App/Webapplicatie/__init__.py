from flask import *
from flask_sqlalchemy import *
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'd42cee127ae26605af73cc0365302fc5'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"