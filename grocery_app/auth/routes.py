from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_required, login_user, logout_user
from grocery_app.models import User
from grocery_app.forms import SignUpForm, LoginForm
# from grocery_app import bcrypt

# Import app and db from events_app package so that we can run app
from grocery_app import app, db

auth = Blueprint("auth", __name__)

##########################################
#           Auth Routes                  #
##########################################


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)

            # Since the next param wasn't present with the default code I did some looking
            # to figure out why:

            # flask's next will not be present if an action is specified in the html form
            # Ex: bad: <form action="/login" good: <form>

            # alternatively you can use: action="{{ url_for('auth.login', next=request.args.get("next")) }}"
            # which will preserve the next param
            # https://stackoverflow.com/questions/36269485/how-do-i-pass-through-the-next-url-with-flask-and-flask-login
            
            next_page = request.args.get('next')

            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))