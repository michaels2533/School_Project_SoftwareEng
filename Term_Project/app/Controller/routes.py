from __future__ import print_function
import re
import sys
from threading import setprofile
from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_wtf.form import FlaskForm
from wtforms.widgets.core import ListWidget
from config import Config
from app import db
from app.Controller.forms import PostForm, ApplicationForm, EditForm, RecommendedSearchForm, SortForm, TagForm
from app.Model.models import Post, Application, Student, Tag, User
from app.Controller.forms import FacultyEditForm, PostForm, ApplicationForm, EditForm, StudentEditForm, ApplicationStatusForm
from app.Model.models import Post, Application

from flask_login import current_user, login_required

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route("/", methods = ['GET'])
@bp_routes.route("/index", methods = ['GET', 'POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    rform = RecommendedSearchForm()
    if current_user.userType == "student":

        if rform.validate_on_submit():

            if rform.boolField.data == True:
                recommended = []
                postFields = []

                # student = Student.query.filter_by(id = current_user.id).first()

                student_interests = [ rt.name for rt in current_user.researchtopic_tag.all()]
                
                print(student_interests)
                for post in posts:
                    for field in post.researchFields:
                        if str(field) in student_interests:
                            recommended.append(post)
                            break

                return render_template('index.html', title = 'Research Postings Portal', posts = recommended, form = rform)

                
    # return render_template('index.html', title = 'Research Postings Portal', posts = posts.all(), form = rform)
    user = User.query.filter_by(id = current_user.id)
    return render_template('index.html', title = 'Research Postings Portal', posts = posts.all(), user = user, form = rform)

@bp_routes.route("/createpost", methods = ['GET', 'POST'])
@login_required
def createPost():
    pform = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    if pform.validate_on_submit():
        newPost = Post(title = pform.title.data, description = pform.description.data, startDate = pform.start.data, endDate = pform.end.data, requiredTime = pform.requiredTime.data
        , qualifications = pform.qualifications.data, facultyFirst = current_user.firstname, facultyLast = current_user.lastname, facultyEmail = current_user.email, 
        facultyUsername = current_user.username)
        for t in pform.researchFields.data:
            newPost.researchFields.append(t)
        db.session.add(newPost)
        db.session.commit()
        flash('Your Research post has be created!')
        return redirect(url_for('routes.index'))
    return render_template('createPost.html', form = pform, posts=posts.all())

@bp_routes.route("/deletePost/<post_id>", methods = ['GET','DELETE', 'POST'])
@login_required
def deletePost(post_id):
    post = Post.query.filter_by(id = post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('Your Research post has been DELETED!')
    return redirect(url_for('routes.index'))

@bp_routes.route("/createApplication/<post_id>/<student_id>", methods = ['GET', 'POST'])
@login_required
def createApplication(post_id, student_id):
    aform = ApplicationForm()
    if aform.validate_on_submit():
        cPost = Post.query.filter_by(id = post_id).first()
        studentWhoApplied = Student.query.filter_by(id = student_id).first()
        #Create new application instance 
        newApplication = Application(firstName = aform.firstName.data, lastName = aform.lastName.data, email = aform.email.data, body = aform.body.data, student_id = current_user.id, username = cPost.facultyUsername, appStatus = 'Pending')
        # newApplication = Application(firstName = aform.firstName.data, lastName = aform.lastName.data,
        #                              email = aform.email.data, body = aform.body.data, username = cPost.facultyUsername)
        newApplication.jobPost = cPost
        newApplication.whoApplied = studentWhoApplied
        #newApplication.writer = current_user; 
        #Saves the Application to the database
        db.session.add(newApplication)
        db.session.commit()
        flash('Your Application has be submitted!')
        return redirect(url_for('routes.index'))
    return render_template('createApplication.html', form = aform)

@bp_routes.route('/withdrawApplication/<post_id>', methods = ['GET', 'POST'])
@login_required
def withdrawApplication(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        flash('Class with id "{}" not found.'.format(post_id))
        return redirect(url_for('routes.index'))

    current_user.withdraw(post)
    db.session.commit()
    flash('You have withdrew your application from {}!'.format(post.title))
    return redirect(url_for('routes.index'))

@bp_routes.route('/display_profile/<uid>/<aid>', methods = ['GET'])
@login_required
def display_profile(uid,aid):
    application = Application.query.all()
    userProfile = User.query.filter_by(id = uid).first()
    if int(aid) > 0: ##if not displaying application information, aid is assigned to -1 
        application = Application.query.filter_by(id = aid).first()

    #applicant = Application.query.filter_by(student_id = id).filter_by().first() # having an issue where I can sort by student, but not by post. so it prints out same reference per same student
    if userProfile.userType == "student":
        return render_template('studentDisplayProfile.html',title = 'Display Profile', student = userProfile, reference = application)
    if userProfile.userType == "Faculty":
        return render_template('facultyDisplayProfile.html',title = 'Display Profile', faculty = userProfile)
    return
   
@bp_routes.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.userType == "student":  
        return redirect(url_for('routes.student_edit_profile'))
    if current_user.userType == "faculty":
        return redirect(url_for('routes.faculty_edit_profile'))

    return redirect(url_for('routes.display_profile', uid = current_user.id, aid = -1))

@bp_routes.route('/faculty_edit_profile', methods = ['GET', 'POST'])
@login_required
def faculty_edit_profile():
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
            return redirect(url_for('routes.display_profile', uid = current_user.id, aid = -1))
    elif request.method == 'GET':
        #populate the user data from DB
        fform.firstname.data = current_user.firstname
        fform.lastname.data = current_user.lastname
        fform.email.data = current_user.email
        fform.officehours.data = current_user.officehours
        
    return render_template('facultyEditProfile.html', title = 'Edit Profile', form = fform)      

@bp_routes.route('/student_edit_profile', methods = ['GET', 'POST'])
@login_required
def student_edit_profile():
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
            return redirect(url_for('routes.display_profile', uid = current_user.id, aid = -1))
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

@bp_routes.route("/appliedStatus/<aid>", methods = ['GET', 'POST'])
@login_required
def appliedStatus(aid):
    aform = ApplicationStatusForm()
    application = Application.query.all()
    sform = SortForm()
    if request.method == 'POST':
        if sform.choice.data == True:
            application = Application.query.filter_by(username = current_user.username)
            return render_template('applied.html', title = 'Applied Students', applicants = application, form = sform, aform = aform)
        qApp = Application.query.filter_by(id = aid).first() 
        qApp.appStatus = aform.statusfield.data
        db.session.commit()
    return render_template('applied.html', title = 'Applied Students', applicants = application, form = sform, aform = aform)

#This is for student
@bp_routes.route("/applicationStatus/", methods = ['GET', 'POST'])
@login_required
def applicationStatus():
    application = Application.query.filter_by(whoApplied = current_user).all()
    return render_template('application.html', title = 'Open Applications', applicant = application)

#This is for faculty
@bp_routes.route("/updateApplication/<aid>", methods = ['POST'])
@login_required
def updateApplication(aid):
     qApp = Application.query.filter_by(id = aid).first() 
     qApp.appStatus = 'Approved for interview'
     qApp.approved = True
     db.session.commit()
     return redirect(url_for('routes.appliedStatus', aid = aid))
