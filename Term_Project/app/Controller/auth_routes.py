from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_sqlalchemy import sqlalchemy
from app.Controller.auth_forms import LoginForm, RegistrationForm
from app.Model.models import Faculty, Student, User
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm, RegistrationForm

from config import Config
from app import db

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        if(User.query.filter_by(email = rform.email.data).count() < 1):
            if rform.userType.data == "Student":
                studentUser = Student(username = rform.username.data, firstname = rform.firstname.data, lastname = rform.lastname.data, email = rform.email.data)
                studentUser.set_password(rform.password.data)
                db.session.add(studentUser)
                db.session.commit()
                flash("Congrats, you are now registered!")
                login_user(studentUser)
                return redirect(url_for('routes.edit_profile'))

            if rform.userType.data == "Faculty":
                facultyUser = Faculty(username = rform.username.data, firstname = rform.firstname.data, lastname = rform.lastname.data, email = rform.email.data)
                facultyUser.set_password(rform.password.data)
                db.session.add(facultyUser)
                db.session.commit()
                flash("Congrats, you are now registered!")
                login_user(facultyUser)
                return redirect(url_for('routes.edit_profile'))
        else:
            flash('The email address you selected is already in use')

    return render_template('register.html', form = rform)


@bp_auth.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('routes.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username =lform.username.data).first()
        if (user is None) or (user.get_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        
        return redirect(url_for('routes.index'))
    return render_template('login.html', title = 'Sign In', form = lform)


@bp_auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))
