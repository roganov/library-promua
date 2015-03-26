from app import db

from . import TestCase
from ..models import Author, Book, User, get_or_build

class BookTest(TestCase):
    def test_unicode(self):
        b = Book(title='Test')
        self.assertEqual(unicode(b), u'Test')

class UserTest(TestCase):
    def test_check_password(self):
        u = User('email@mail.com', 'pwd')
        self.assertTrue(u.check_password('pwd'))
        self.assertFalse(u.check_password('ppwwdd'))


class AuthorTest(TestCase):
    def test_get_or_build(self):
        a = Author(name='Author')
        db.session.add(a)
        db.session.commit()
        a2 = get_or_build(Author, name='Author')
        self.assertEqual(a.id, a2.id)
        a3 = get_or_build(Author, name='Author3')
        self.assertIsNone(a3.id)
