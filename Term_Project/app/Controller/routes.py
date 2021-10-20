from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, redirect, url_for, flash
from config import Config

from app import db
from app.Controller.forms import PostForm
from app.Model.models import Post

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route("/", methods = ['GET'])
@bp_routes.route("/index", methods = ['GET', 'POST'])
# add @login_required here
def index():
    posts = Post.query.order_by(Post.timestamp.desc())

    return render_template('index.html', title = 'Research Postings Portal', posts = posts.all())

@bp_routes.route("/createpost", methods = ['GET', 'POST'])
def createPost():
    pform = PostForm()
    if pform.validate_on_submit():
        newPost = Post(title = pform.title.data, body = pform.body.data)
        db.session.add(newPost)
        db.session.commit()
        flash('Your Research post has be created!')
        return redirect(url_for('routes.index'))
    return render_template('createPost.html', form = pform)