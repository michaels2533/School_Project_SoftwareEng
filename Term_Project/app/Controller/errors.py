from flask import Blueprint, render_template, request
from app import db

bp_errors = Blueprint('errors', __name__)

#will handle page not found errors
@bp_errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('404error.html'), 404

#will handle internal server errors
@bp_errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500error.html'), 500