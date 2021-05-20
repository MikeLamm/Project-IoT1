from Webapplicatie import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager

class Verblijf(db.Model):

    __tablename__ = "Verblijf"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Diersoort(db.Model):

    __tablename__ = "Diersoort"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    

    def __init__(self, name):
        self.name = name
        
class Device(db.Model):

    __tablename__ = "Device"
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.Text)

    def __init__(self, address):
        self.address = address

class Dier(db.Model):

    __tablename__ = "Dier"
    id = db.Column(db.Integer, primary_key = True)
    soort = db.Column(db.Integer, db.ForeignKey("Diersoort.id"))
    name = db.Column(db.Text)   
    detected = db.Column(db.Boolean)
    device = db.Column(db.Integer, db.ForeignKey("Device.id"))
    verblijf = db.Column(db.Integer,db.ForeignKey("Verblijf.id"))

    def __init__(self, soort, name, detected, device, verblijf):
        self.soort = Diersoort.query.filter_by(name=soort).first().id
        self.name = name
        self.detected = detected
        self.device = device
        self.verblijf = Verblijf.query.filter_by(name=verblijf).first().id

class Sensor(db.Model):

    __tablename__ = "Sensor"
    id = db.Column(db.Integer, primary_key = True)
    verblijf = db.Column(db.Integer, db.ForeignKey("Verblijf.id"))
    x = db.Column(db.Float)
    y = db.Column(db.Float)

    def __init__(self, verblijf, x, y):
        self.verblijf = verblijf
        self.x = x
        self.y = y

class Data(db.Model):

    __tablename__ = "Data"
    id = db.Column(db.Integer, primary_key = True)
    sensor = db.Column(db.Integer, db.ForeignKey("Sensor.id"))
    dier = db.Column(db.Text,db.ForeignKey("Dier.id"))
    output = db.Column(db.Float)

    def __init__(self, sensor, dier, output):
        self.sensor = sensor
        self.dier = dier
        self.output = output

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean())

    def __init__(self, email, username, password, first_name, last_name, tel):
            self.email = email
            self.username = username
            self.password_hash = generate_password_hash(password)
            self.first_name = first_name
            self.last_name = last_name
            self.tel = tel
            self.admin = False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)