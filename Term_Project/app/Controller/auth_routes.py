from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, redirect, url_for
from config import Config

from app import db

bp_auth_routes = Blueprint('auth_routes', __name__)
bp_auth_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'