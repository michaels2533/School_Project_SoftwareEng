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
        p1 = Post(title='My post', description='This is my test post.',startDate = '12/05/2021',endDate = '12/16/2021', requiredTime=5, user_id=u1.id)
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().title, 'My post')
        self.assertEqual(u1.get_user_posts().first().description, 'This is my test post.')
        self.assertEqual(u1.get_user_posts().first().requiredTime, 5)

    def test_post_2(self):
        u1 = User(username='john', firstname = 'john', lastname = 'cena' ,email='john.cena@wsu.com', userType = 'faculty')
        u2 = User(username='jared', firstname = 'jared', lastname = 'lustig' ,email='jared.lustig@wsu.com', userType = 'faculty')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        self.assertEqual(u2.get_user_posts().all(), [])
        p1 = Post(title='My post 1', description='This is my first test post.', requiredTime=5, user_id=u1.id)
        db.session.add(p1)
        p2 = Post(title='My post 2', description='This is my second test post.', requiredTime=5, user_id=u1.id)
        db.session.add(p2)
        db.session.commit()
        p3 = Post(title='Another post', description='This is a post by somebody else.', requiredTime=5, user_id=u2.id)
        db.session.add(p3)
        db.session.commit()
        # test the posts by the first user
        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[1].title, 'My post 2')
        self.assertEqual(u1.get_user_posts().all()[1].description, 'This is my second test post.')
        self.assertEqual(u1.get_user_posts().all()[1].requiredTime, 5)
        # test the posts by the second user
        self.assertEqual(u2.get_user_posts().count(), 1)
        self.assertEqual(u2.get_user_posts().all()[0].title, 'Another post')
        self.assertEqual(u2.get_user_posts().all()[0].description, 'This is a post by somebody else.')
        self.assertEqual(u2.get_user_posts().all()[0].requiredTime, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)