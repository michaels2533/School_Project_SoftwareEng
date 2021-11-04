from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from config import Config

from app import db
from app.Controller.forms import PostForm, ApplicationForm, EditForm, TagForm
from app.Model.models import Post, Application, Tag

from flask_login import current_user, login_required

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route("/", methods = ['GET'])
@bp_routes.route("/index", methods = ['GET', 'POST'])
# add @login_required here
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())

    return render_template('index.html', title = 'Research Postings Portal', posts = posts.all())

@bp_routes.route("/createpost", methods = ['GET', 'POST'])
@login_required
def createPost():
    pform = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    if pform.validate_on_submit():
        newPost = Post(title = pform.title.data, description = pform.description.data, startDate = pform.start.data, endDate = pform.end.data, requiredTime = pform.requiredTime.data
        , qualifications = pform.qualifications.data)
        for t in pform.researchFields.data:
            newPost.researchFields.append(t)
        db.session.add(newPost)
        db.session.commit()
        flash('Your Research post has be created!')
        return redirect(url_for('routes.index'))
    return render_template('createPost.html', form = pform, posts=posts.all())

@bp_routes.route("/createApplication/<post_id>", methods = ['GET', 'POST'])
@login_required
def createApplication(post_id):
    aform = ApplicationForm()
    addTag = TagForm()
    if aform.validate_on_submit():
        # if addTag.validate_on_submit():
        #     addTag = Tag(name = addTag.newField.data)
        #     db.session.add(addTag)
        #     db.session.commit()

        cPost = Post.query.filter_by(id = post_id).first()
        #Create new application instance 
        newApplication = Application(firstName = aform.firstName.data, lastName = aform.lastName.data, email = aform.email.data, phoneNum = aform.phoneNum.data, body = aform.body.data)
        newApplication.jobPost = cPost
        #Saves the Application to the database
        db.session.add(newApplication)
        db.session.commit()
        flash('Your Application has be submitted!')
        return redirect(url_for('routes.index'))
    return render_template('_createApplication.html', form = aform, tagForm = addTag)

@bp_routes.route('/addTag', methods = ['GET', 'POST'])
@login_required
def addTag():
    addTag = TagForm()
    allTags = Tag.query.all()
    if addTag.validate_on_submit():
        addTag = Tag(name = addTag.newField.data)
        if allTags == []:
            db.session.add(addTag)
            db.session.commit()
        for t in allTags:
            if addTag.name == t.name:
                flash('Already a Research Tag')
                break     
            else:
                db.session.add(addTag)
                db.session.commit()
        return redirect(url_for('routes.createPost'))
    return render_template('createtag.html', form = addTag)

@bp_routes.route('/display_profile', methods = ['GET'])
@login_required
def display_profile():
    return render_template('displayProfile.html',title = 'Display Profile', student = current_user)

@bp_routes.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    eform = EditForm()
    if request.method == 'POST':
        #handle the form submission
        if eform.validate_on_submit():
            current_user.firstname = eform.firstname.data
            current_user.lastname = eform.lastname.data
            current_user.email = eform.email.data
            current_user.set_password(eform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Your changes have been saved!")
            return redirect(url_for('routes.display_profile'))
    elif request.method == 'GET':
        #populate the user data from DB
        eform.firstname.data = current_user.firstname
        eform.lastname.data = current_user.lastname
        eform.email.data = current_user.email
    else:
        pass
    return render_template('editProfile.html', title = 'Edit Profile', form = eform)