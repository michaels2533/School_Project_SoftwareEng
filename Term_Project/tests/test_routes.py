"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.Model.models import Post, Application, Student, Tag, User, Faculty, ElectiveTag,ResearchTopicTag, ProgramLanguageTag
from config import Config

import unittest

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True


@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_student(sname,sfirstname,slastname,semail, passwd):
    student = Student(username=sname, firstname = sfirstname,lastname = slastname ,email=semail)
    student.set_password(passwd)
    return student

def new_faculty(fname,ffirstname,flastname,femail, passwd):
    faculty = Faculty(username=fname, firstname = ffirstname,lastname = flastname ,email=femail)
    faculty.set_password(passwd)
    return faculty

def init_tags():
    # initialize the tags
    if Tag.query.count() == 0:
        tags = ['Data Structures','Machine Learning', 'High Performance Computing', 'Web Development', 'Computer Achitecture']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()
    # initialize the elective tags
    if ElectiveTag.query.count() == 0:
        eTag = ['AI', 'Machine Learning', 'Neural Networks', 'Database Systems', 'Security']
        for e in eTag:
            db.session.add(ElectiveTag(name = e))
        db.session.commit()
    # initialize the program language tags
    if ProgramLanguageTag.query.count() == 0:
        pTag = ['Python', 'C/C++', 'C#','Java', 'JavaScript', 'Golang']
        for p in pTag:
            db.session.add(ProgramLanguageTag(name = p))
        db.session.commit()
    # initialize the research topic tags
    if ResearchTopicTag.query.count() == 0:
        rTag =  ['Data Structures', 'Machine Learning', 'High Perfomance Computing', 'Web Development', 'Computer Architecture']
        for r in rTag:
            db.session.add(ResearchTopicTag(name = r))
        db.session.commit()
        
    return None

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    # initialize the tags
    init_tags()
    #add a student    
    student1 = new_student(sname='student1',sfirstname='student1',slastname='student1',semail='student1@wsu.edu',passwd='1234')
    #adds a faculty 
    faculty1 = new_faculty(fname='faculty1',ffirstname='faculty1',flastname='faculty1',femail='faculty1@wsu.edu',passwd='1234')
    # Insert user data
    db.session.add(student1)
    db.session.add(faculty1)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """ 
    
    init_database()

    # Create a test client using the Flask application configured for testing
    response = test_client.post('/register', 
                          data=dict(username='student2', password='1234',firstname = 'student2',lastname = 'student2',email = 'student2@wsu.edu',userType = 'Student'),
                          follow_redirects = True)


    assert response.status_code == 200

    s = db.session.query(Student).filter(Student.username =='john')
    assert s.first().email == 'john@wsu.edu'
    assert s.count() == 1
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data

def test_invalidlogin(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(username='jared1', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login', 
                          data=dict(username='student1', password='1234',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to WSU Research Openings!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Please log in to access this page." in response.data    

def test_createPost(test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/postsmile' page is requested (GET)  AND /PostForm' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #login
    response = test_client.post('/login', 
                        data=dict(username='faculty1', password='1234'),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to WSU Research Openings!" in response.data
    
    #test the Createpost form 
    response = test_client.get('/createpost')
    assert response.status_code == 200
    assert b"Post New Research Position" in response.data
    
    #test posting a research position
    tags1 = list( map(lambda t: t.id, Tag.query.all()[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    print("TESTING********************: ", tags1)
    response = test_client.post('/createpost', 
                          data=dict(title='faculty1 test post', description='faculty1 test1',startDate = '5/7/22',endDate = '5/12/22',requiredTime = '5 hours',qualifications = "faculty1 qualifications", tag = tags1),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Post New Research Position" in response.data


    c = db.session.query(Post).filter(Post.title =='faculty1 test post')
    assert c.first().get_tags().count() == 3 #should have 3 tags
    assert c.count() >= 1 


    tags2 = list( map(lambda t: t.id, Tag.query.all()[1:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    print("TESTING********************: ", tags2)
    response = test_client.post('/createpost', 
                          data=dict(title='faculty1 test post2', description='faculty1 test2',startDate = '5/7/22',endDate = '5/12/22',requiredTime = '5 hours',qualifications = "faculty1 qualifications", tag = tags2),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Post New Research Position" in response.data


    c = db.session.query(Post).filter(Post.title =='faculty1 test post2')
    assert c.first().get_tags().count() == 2  # Should have 2 tags
    assert c.count() >= 1 

    assert db.session.query(Post).count() == 2

    #finally logout
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Please log in to access this page." in response.data   

def test_deletePost(test_client,init_database):
  
    #login
    response = test_client.post('/login', 
                        data=dict(username='faculty1', password='1234'),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to WSU Research Openings!" in response.data
    
    #first post a research positions
    tags1 = list( map(lambda t: t.id, Tag.query.all()[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    response = test_client.post('/createpost', 
                          data=dict(title='faculty1 test post', description='faculty1 test1',startDate = '5/7/22',endDate = '5/12/22',requiredTime = '5 hours',qualifications = "faculty1 qualifications", tag = tags1),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Post New Research Position" in response.data
    

    c = db.session.query(Post).filter(Post.title == 'faculty test post').first()

    #Deletes the post based on the id
    reponse = test_client.post('/deletePost',data = dict(post_id = c.id),follow_redirects = True)
    assert response.status_code == 200
    assert b"Your Resarch post has been DELETED!" 

if __name__ == '__main__':
    unittest.main(verbosity=2)