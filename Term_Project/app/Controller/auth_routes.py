from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from flask_sqlalchemy import sqlalchemy
from app.Controller.auth_forms import LoginForm, RegistrationForm
from app.Model.models import User
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
        user = User(username = rform.username.data, email = rform.email.data)
        user.set_password(rform.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats, you are now registered!")
        return redirect(url_for('routes.index'))
    return render_template('register.html', form = rform)