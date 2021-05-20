from wtforms import *
from wtforms.validators import *
from flask_wtf import FlaskForm
from Webapplicatie import db
from Webapplicatie.models import *

class login_form(FlaskForm):
    password = PasswordField('Wachtwoord: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email(message='Voer een geldig emailadres in!')])
    submit = SubmitField('Log in')

class register_form(FlaskForm):
    username = StringField('Gebruikersnaam: ', validators=[DataRequired()])
    first_name = StringField('Voornaam: ', validators=[DataRequired()])
    last_name = StringField('Achternaam: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email(message='Voer een geldig emailadres in!')])
    password = PasswordField('Wachtwoord: ', validators=[DataRequired(), EqualTo('confirm', message='De wachtwoorden komen niet overeen!')])
    confirm = PasswordField('Herhaal uw wachtwoord: ', validators=[DataRequired()])
    tel = IntegerField('Telefoonnummer:', validators=[DataRequired()])
    submit = SubmitField('Registreer')

class change_password(FlaskForm):
    password = PasswordField('Wachtwoord: ', validators=[DataRequired(), EqualTo('confirm', message='De wachtwoorden komen niet overeen!')])
    confirm = PasswordField('Herhaal uw wachtwoord: ', validators=[DataRequired()])
    submit = SubmitField('Wijzig wachtwoord')

class add_stay(FlaskForm):
    stay = StringField(validators=[DataRequired()])
    submit = SubmitField('Voeg verblijf toe')

class change_stay(FlaskForm):
    cur = StringField('Huidige naam: ')
    stay = StringField('Nieuwe naam: ', validators=[DataRequired()])
    submit = SubmitField('Wijzig verblijf.')
    
class add_animal(FlaskForm):
    naam = StringField('Naam:')
    soort = SelectField('Soort: ', choices=[(i.name, i.name) for i in Diersoort.query.all()])
    device = SelectField('Device ID:', choices=[(i.address, i.address) for i in Device.query.all()])
    verblijf = SelectField('Verblijf', choices=[(i.name, i.name) for i in Verblijf.query.all()])
    submit = SubmitField('Voeg dier toe')

class AuthForm(FlaskForm):
    code = StringField('Authenticatiecode:')
    submit = SubmitField()