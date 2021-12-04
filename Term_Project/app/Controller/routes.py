from __future__ import print_function
import re
import sys
from threading import setprofile
from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_wtf.form import FlaskForm
from config import Config
from app import db
from app.Controller.forms import PostForm, ApplicationForm, EditForm, TagForm
from app.Model.models import Post, Application, Student, Tag
from app.Controller.forms import FacultyEditForm, PostForm, ApplicationForm, EditForm, StudentEditForm
from app.Model.models import Post, Application, User

from flask_login import current_user, login_required

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route("/", methods = ['GET'])
@bp_routes.route("/index", methods = ['GET', 'POST'])
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
        , qualifications = pform.qualifications.data, facultyFirst = current_user.firstname, facultyLast = current_user.lastname, facultyEmail = current_user.email)
        for t in pform.researchFields.data:
            newPost.researchFields.append(t)
        db.session.add(newPost)
        db.session.commit()
        flash('Your Research post has be created!')
        return redirect(url_for('routes.index'))
    return render_template('createPost.html', form = pform, posts=posts.all())

@bp_routes.route("/createApplication/<post_id>/<student_id>", methods = ['GET', 'POST'])
@login_required
def createApplication(post_id, student_id):
    aform = ApplicationForm()
    if aform.validate_on_submit():
        cPost = Post.query.filter_by(id = post_id).first()
        studentWhoApplied = Student.query.filter_by(id = student_id).first()
        #Create new application instance 
        newApplication = Application(firstName = aform.firstName.data, lastName = aform.lastName.data, email = aform.email.data, body = aform.body.data)
        newApplication.jobPost = cPost
        newApplication.whoApplied = studentWhoApplied
        #Saves the Application to the database
        db.session.add(newApplication)
        db.session.commit()
        flash('Your Application has be submitted!')
        return redirect(url_for('routes.index'))
    return render_template('createApplication.html', form = aform)

@bp_routes.route('/display_profile/<id>', methods = ['GET'])
@login_required
def display_profile(id):
    if current_user.userType == "Student":
        # return redirect(url_for('routes.student_display_profile', id))
        viewStudent = Student.query.filter_by(id = id).first()
        return render_template('studentDisplayProfile.html',title = 'Display Profile', student = current_user, viewer = viewStudent)
    if current_user.userType == "Faculty":
        # return redirect(url_for('routes.faculty_display_profile'))
        return render_template('facultyDisplayProfile.html',title = 'Display Profile', faculty = current_user)
    return

    
@bp_routes.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.userType == "faculty":  #if editing a student profile
        # return redirect(url_for('routes.student_edit_profile'))
        fform = FacultyEditForm()
        if request.method == 'POST':
            #handle the form submission    
                current_user.firstname = fform.firstname.data
                current_user.lastname = fform.lastname.data
                current_user.email = fform.email.data
                current_user.officehours = fform.officehours.data
                current_user.set_password(fform.password.data)
                db.session.add(current_user)
                db.session.commit()
                flash("Your changes have been saved!")
                return redirect(url_for('routes.display_profile'))
        elif request.method == 'GET':
            #populate the user data from DB
            fform.firstname.data = current_user.firstname
            fform.lastname.data = current_user.lastname
            fform.email.data = current_user.email
            fform.officehours.data = current_user.officehours
            
        return render_template('facultyEditProfile.html', title = 'Edit Profile', form = fform)
    
    if current_user.userType == "student": #if editing a faculty profile
        # return redirect(url_for('routes.faculty_edit_profile'))
        sform = StudentEditForm()
        if request.method == 'POST':
            #handle the form submission    
                current_user.firstname = sform.firstname.data
                current_user.lastname = sform.lastname.data
                current_user.email = sform.email.data
                current_user.major = sform.major.data
                current_user.GPA = sform.GPA.data
                current_user.gradDate = sform.gradDate.data
                # current_user.electives = sform.electives.data
                for i in sform.electives.data:
                    current_user.elective_tag.append(i)
                #current_user.researchTopics = sform.researchTopics.data
                for i in sform.researchTopics.data:
                    current_user.researchtopic_tag.append(i)
                # current_user.programLanguages = sform.programLanguages.data
                for i in sform.programLanguages.data:
                    current_user.programlangauge_tag.append(i)

                current_user.experience = sform.experience.data
                current_user.set_password(sform.password.data)
                db.session.add(current_user)
                db.session.commit()
                flash("Your changes have been saved!")
                return redirect(url_for('routes.display_profile', id = current_user.id))
        elif request.method == 'GET':
            #populate the user data from DB
            sform.firstname.data = current_user.firstname
            sform.lastname.data = current_user.lastname
            sform.email.data = current_user.email
            sform.major.data = current_user.major
            sform.GPA.data = current_user.GPA
            sform.gradDate.data = current_user.gradDate
            # sform.electives.data = current_user.electives
            for i in sform.electives.data:
                sform.electives.data = current_user.electives
            #sform.researchTopics.data = current_user.researchTopics
            for i in sform.researchTopics.data:
                sform.researchTopics = current_user.researchtopics
            #sform.programLanguages.data = current_user.programLanguages
            for i in sform.programLanguages.data:
                sform.programLanguages.data = current_user.programlanguages
            sform.experience.data = current_user.experience

        else:
            pass
        return render_template('studentEditProfile.html', title = 'Edit Profile', form = sform)

    return redirect(url_for('routes.display_profile', current_user.id))    

@bp_routes.route("/appliedStatus/", methods = ['GET', 'POST'])
@login_required
def appliedStatus():
    appliedpost = Post.query.all()
    appliedStudent = Application.query.all()
    return render_template('applied.html', title = 'Applied Students', post = appliedpost, applied = appliedStudent)