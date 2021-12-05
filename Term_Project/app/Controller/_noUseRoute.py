# @bp_routes.route('/addTag', methods = ['GET', 'POST'])
# @login_required
# def addTag():
#     addTag = TagForm()
#     allTags = Tag.query.all()
#     if addTag.validate_on_submit():
#         addTag = Tag(name = addTag.newField.data)
#         if allTags == []:
#             db.session.add(addTag)
#             db.session.commit()
#         for t in allTags:
#             if addTag.name == t.name:
#                 flash('Already a Research Tag')
#                 break     
#             else:
#                 db.session.add(addTag)
#                 db.session.commit()
#         return redirect(url_for('routes.display_profile'))
#     return render_template('createtag.html', form = addTag)


# @bp_routes.route('/student_edit_profile', methods = ['GET', 'POST'])
# @login_required
# def student_edit_profile():
#     sform = StudentEditForm()
#     if request.method == 'POST':
#         #handle the form submission    
#             current_user.firstname = sform.firstname.data
#             current_user.lastname = sform.lastname.data
#             current_user.email = sform.email.data
#             current_user.major = sform.major.data
#             current_user.GPA = sform.GPA.data
#             current_user.gradDate = sform.gradDate.data
#             # current_user.electives = sform.electives.data
#             for i in sform.electives.data:
#                 current_user.elective_tag.append(i)
#             #current_user.researchTopics = sform.researchTopics.data
#             for i in sform.researchTopics.data:
#                 current_user.researchtopic_tag.append(i)
#             # current_user.programLanguages = sform.programLanguages.data
#             for i in sform.programLanguages.data:
#                 current_user.programlangauge_tag.append(i)

#             current_user.experience = sform.experience.data
#             current_user.set_password(sform.password.data)
#             db.session.add(current_user)
#             db.session.commit()
#             flash("Your changes have been saved!")
#             return redirect(url_for('routes.student_display_profile', id = current_user.id))
#     elif request.method == 'GET':
#         #populate the user data from DB
#         sform.firstname.data = current_user.firstname
#         sform.lastname.data = current_user.lastname
#         sform.email.data = current_user.email
#         sform.major.data = current_user.major
#         sform.GPA.data = current_user.GPA
#         sform.gradDate.data = current_user.gradDate
#         # sform.electives.data = current_user.electives
#         for i in sform.electives.data:
#             sform.electives.data = current_user.electives
#         #sform.researchTopics.data = current_user.researchTopics
#         for i in sform.researchTopics.data:
#             sform.researchTopics = current_user.researchtopics
#         #sform.programLanguages.data = current_user.programLanguages
#         for i in sform.programLanguages.data:
#             sform.programLanguages.data = current_user.programlanguages
#         sform.experience.data = current_user.experience

#     else:
#         pass
#     return render_template('studentEditProfile.html', title = 'Edit Profile', form = sform)

# @bp_routes.route('/faculty_edit_profile', methods = ['GET', 'POST'])
# @login_required
# def faculty_edit_profile():
#     fform = FacultyEditForm()
#     if request.method == 'POST':
#         #handle the form submission    
#             current_user.firstname = fform.firstname.data
#             current_user.lastname = fform.lastname.data
#             current_user.email = fform.email.data
#             current_user.officehours = fform.officehours.data
#             current_user.set_password(fform.password.data)
#             db.session.add(current_user)
#             db.session.commit()
#             flash("Your changes have been saved!")
#             return redirect(url_for('routes.faculty_display_profile'))
#     elif request.method == 'GET':
#         #populate the user data from DB
#         fform.firstname.data = current_user.firstname
#         fform.lastname.data = current_user.lastname
#         fform.email.data = current_user.email
#         fform.officehours.data = current_user.officehours
        
#     return render_template('facultyEditProfile.html', title = 'Edit Profile', form = fform)  

# @bp_routes.route('/student_display_profile/<id>', methods = ['GET'])
# @login_required
# def student_display_profile(id):
#     viewStudent = Student.query.filter_by(id = id).first()
#     return render_template('studentDisplayProfile.html',title = 'Display Profile', student = current_user, viewer = viewStudent)

# @bp_routes.route('/faculty_display_profile', methods = ['GET'])
# @login_required
# def faculty_display_profile():
#     return render_template('facultyDisplayProfile.html',title = 'Display Profile', faculty = current_user)

""" The stuff bellow is for display profile, if the user was a student"""

 