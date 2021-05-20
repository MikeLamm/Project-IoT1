from Webapplicatie import app, db, message
from Webapplicatie.models import *
from Webapplicatie.forms import *
from Webapplicatie.TFA import *
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, redirect, url_for, request, flash

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    residences = Verblijf.query.all()
    animals = Dier.query.all()
    
    d = {}
    path = []
    missing_animals = {}
    for i in residences:
        print(i.name)
        path.append(f'static/maps/{i.name}.png')
        print(path)
        d[i.id] = []
        missing_animals[i.id] = []
        # print(missing_animals.keys())
        soort = Dier.query.filter_by(verblijf=i.id).all()
        L = [k for k in soort if k.detected == False]
        for k in Dier.query.filter_by(verblijf=i.id, detected=False).all():
            print(i.id)
            if k.detected == False and k is not None:
                missing_animals[i.id] += [k]
        print(missing_animals)

        for j in soort:
            d[i.id] += [k for k in animals if k.id == j.id and k.detected == True]


    soorten = {}
    for i in Diersoort.query.all():
        soorten[i.id] = ''
        soorten[i.id] += i.name

    return render_template('home.html', residence=residences, list_of_animals=d, soorten=soorten, missing_animals=missing_animals, path=path)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                global auth 
                auth = Two_Factor_Auth(user)
                auth = auth.send_code()
                return redirect(f'/auth/{user.id}')
            else:
                error = 'De ingevoerde gegevens zijn niet correct.'
        else:
            error = 'Er bestaat geen account met deze inloggegevens'
    return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = register_form()
    error = ''
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None and User.query.filter_by(email=form.email.data).first() is None:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        tel=form.tel.data)
            db.session.add(user)
            db.session.commit()
            global auth 
            auth = Two_Factor_Auth(user)
            auth = auth.send_code()
            return redirect(f'/auth/{user.id}')
        else:
            error = 'Er bestaat al een account met deze gegevens.'
    return render_template('register.html', form=form, error=error)

@app.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
    admin = current_user.admin
    stays = Verblijf.query.all()
    animals = Dier.query.all()
    sort = Diersoort.query.all()
    change_pw = change_password()
    addstay = add_stay()
    addanimal = add_animal()
    if change_pw.validate_on_submit():
        print('hoi')
        user = User.query.get(current_user.id)
        print(user)
        user.password = change_pw.password.data
        db.session.add(user)
        db.session.commit()
        print('Mooiman')
        return redirect(url_for('dashboard'))
    elif addstay.validate_on_submit():
        stay = Verblijf(addstay.stay.data)
        db.session.add(stay)
        db.session.commit()
        return redirect(url_for('panel'))
    elif addanimal.validate_on_submit():
        animal = Dier(addanimal.soort.data, addanimal.naam.data, False, addanimal.device.data, addanimal.verblijf.data)
        db.session.add(animal)
        db.session.commit()
        return redirect(url_for('panel'))
    return render_template('panel.html', admin=admin, change_pw=change_pw, stays=stays, addstay=addstay, animals=animals, addanimal=addanimal, sort=sort)

@app.route('/rem_stay/<id>')
@login_required
def rem_stay(id):
    stay = Verblijf.query.get(id)
    db.session.delete(stay)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route('/rem_animal/<id>')
@login_required
def rem_animal(id):
    dier = Dier.query.get(id)
    db.session.delete(dier)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route('/rem_sort/<id>')
@login_required
def rem_sort(id):
    sort = Diersoort.query.get(id)
    db.session.delete(sort)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route('/auth/<id>', methods=['GET', 'POST'])
def two_factor_auth(id):
    form = AuthForm()
    user = User.query.get(id)
    print(auth)
    error=''
    if form.validate_on_submit():
        code = form.code.data
        print(code)
        if auth == code:
            login_user(user)
            next = url_for('dashboard')
            return redirect(next)
        else:
            error = 'Verkeerde code ingevoerd. Probeer het opnieuw!'
    return render_template('auth.html', form=form, error=error)


