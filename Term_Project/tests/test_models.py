import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Post, Tag
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='john', firstname = 'john', lastname = 'cena' ,email='john.cena@wsu.com', userType = 'faculty')
        u.set_password('covid')
        self.assertFalse(u.get_password('flu'))
        self.assertTrue(u.get_password('covid'))

    def test_post_1(self):
        u1 = User(username='john', firstname = 'john', lastname = 'cena' ,email='john.cena@wsu.com', userType = 'faculty')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        p1 = Post(title='My post', description='This is my test post.',startDate = '12/05/2021',endDate = '12/16/2021',requiredTime=5, qualifications = 'Being able to Work',
                     user_id=u1.id)
        p1.researchFields.append(Tag(name='Data Structures'))
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().title, 'My post')
        self.assertEqual(u1.get_user_posts().first().description, 'This is my test post.')
        self.assertEqual(u1.get_user_posts().first().startDate, '12/05/2021')
        self.assertEqual(u1.get_user_posts().first().endDate, '12/16/2021')
        self.assertEqual(u1.get_user_posts().first().requiredTime, '5')
        self.assertEqual(u1.get_user_posts().first().qualifications, 'Being able to Work')
        self.assertEqual(u1.get_user_posts().first().get_tags().first().name, 'Data Structures')
        
    def test_post_2(self):
        u1 = User(username='john', firstname = 'john', lastname = 'cena' ,email='john.cena@wsu.com', userType = 'faculty')
        u2 = User(username='jared', firstname = 'jared', lastname = 'lustig' ,email='jared.lustig@wsu.com', userType = 'faculty')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        self.assertEqual(u2.get_user_posts().all(), [])
        p1 = Post(title='My post 1', description='This is my first test post.',startDate = '12/01/2021',
                  endDate = '12/31/2021',requiredTime=10, qualifications = 'Having Flask Expierence',
                   user_id=u1.id)
        p1.researchFields.append(Tag(name='High Performance Computing'))
        db.session.add(p1)
        p2 = Post(title='My post 2', description='This is my second test post.',startDate = '01/01/2022',
                  endDate = '01/16/2022',requiredTime=5, qualifications = 'Having Front Stack Experience',
                  user_id=u1.id)
        p2.researchFields.append(Tag(name='Data Structures'))
        p2.researchFields.append(Tag(name='Web Development'))
        db.session.add(p2)
        db.session.commit()
        p3 = Post(title='Another Post', description='This is a post by somebody else.', startDate = '10/20/2021',
                  endDate = '11/23/2021',requiredTime=15, qualifications = 'Being able to learn',
                   user_id=u2.id)
        p3.researchFields.append(Tag(name='Machine Learning'))
        db.session.add(p3)
        db.session.commit()
        
        # test the posts by the first user - post 1
        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[0].title, 'My post 1')
        self.assertEqual(u1.get_user_posts().all()[0].description, 'This is my first test post.')
        self.assertEqual(u1.get_user_posts().all()[0].startDate, '12/01/2021')
        self.assertEqual(u1.get_user_posts().all()[0].endDate, '12/31/2021')
        self.assertEqual(u1.get_user_posts().all()[0].requiredTime, '10')
        self.assertEqual(u1.get_user_posts().all()[0].qualifications, 'Having Flask Expierence')
        self.assertEqual(u1.get_user_posts().all()[0].get_tags().first().name, 'High Performance Computing')
        # test the posts by the firs user - post 2
        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[1].title, 'My post 2')
        self.assertEqual(u1.get_user_posts().all()[1].description, 'This is my second test post.')
        self.assertEqual(u1.get_user_posts().all()[1].startDate, '01/01/2022')
        self.assertEqual(u1.get_user_posts().all()[1].endDate, '01/16/2022')
        self.assertEqual(u1.get_user_posts().all()[1].requiredTime, '5')
        self.assertEqual(u1.get_user_posts().all()[1].qualifications, 'Having Front Stack Experience')
        self.assertEqual(u1.get_user_posts().all()[1].get_tags().all()[0].name, 'Data Structures')
        self.assertEqual(u1.get_user_posts().all()[1].get_tags().all()[1].name, 'Web Development')
        
        # test the posts by the second user
        self.assertEqual(u2.get_user_posts().count(), 1)
        self.assertEqual(u2.get_user_posts().all()[0].title, 'Another Post')
        self.assertEqual(u2.get_user_posts().all()[0].description, 'This is a post by somebody else.')
        self.assertEqual(u2.get_user_posts().all()[0].startDate, '10/20/2021')
        self.assertEqual(u2.get_user_posts().all()[0].endDate, '11/23/2021')
        self.assertEqual(u2.get_user_posts().all()[0].requiredTime, '15')
        self.assertEqual(u2.get_user_posts().all()[0].qualifications, 'Being able to learn')
        self.assertEqual(u2.get_user_posts().all()[0].get_tags().first().name, 'Machine Learning')
        

if __name__ == '__main__':
    unittest.main(verbosity=2)