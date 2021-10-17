from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, redirect, url_for
from config import Config

from app import db

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route("/", methods = ['GET'])
@bp_routes.route("/index", methods = ['GET', 'POST'])
# add @login_required here
def index():
    #create form for organizing posts
    #all create post model to pass into as form
    #then make sure -> if form.validate_on_submit():
    #pass form into render_template
    return render_template('index.html', title = 'Research Postings Portal')
