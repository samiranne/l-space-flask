# run 'python -m unittest test_app.py'
# 'python -m unittest -v test_app.py' to produce more verbose output
import unittest
from sqlalchemy.exc import IntegrityError
from models import User
from app_factory import create_app


class AppTest(unittest.TestCase):

    def add_to_database(self, object):
        self.db.session.add(object)
        self.db.session.commit()

    def setUp(self):
        self.app, self.db, self.bcrypt, __ = create_app(testing=True)
        from models import User, Book, OwnedBookCopy, House
        self.db.create_all()

    def tearDown(self):
        pass

    def test_create_user(self):
        name = 'test_user'
        email = 'user@test.test'
        password = 'test_password'
        user = User(display_name=name, email=email, password=password)
        self.add_to_database(user)

        self.assertTrue(user in self.db.session)
        user_by_display_name = User.query.filter_by(display_name=name).all()
        self.assertEqual(len(user_by_display_name), 1)
        user_from_db = User.get_user_by_email(email)
        self.assertEqual(user_from_db.email, email)
        self.assertEqual(user_from_db.display_name, name)

    def test_error_when_creating_user_with_existing_email(self):
        self.add_to_database(User(display_name='user', email='email', password='password'))
        l = lambda: self.add_to_database(User(display_name='user2', email='email', password='password2'))
        self.assertRaises(IntegrityError, l)

    def test_user_doesnt_exist_returns_none(self):
        user = User.get_user_by_email("bla")
        self.assertIs(user, None)
        user2 = User.get_user_by_id(100000)
        self.assertIs(user2, None)

if __name__ == '__main__':
    unittest.main()
