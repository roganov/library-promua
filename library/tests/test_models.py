import unittest
from app import app, db

from ..models import Book, User

class TestCase(unittest.TestCase):
    # Testing DB is recreated for every test
    # Better to create the DB once and wrap every test in transaction
    # But for now, let it be
    def setUp(self):
        app.config.from_object('config.TestConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BookTest(TestCase):
    def test_unicode(self):
        b = Book(title='Test')
        self.assertEqual(unicode(b), u'Test')

class UserTest(TestCase):
    def test_check_password(self):
        u = User('email@mail.com', 'pwd')
        self.assertTrue(u.check_password('pwd'))
        self.assertFalse(u.check_password('ppwwdd'))
