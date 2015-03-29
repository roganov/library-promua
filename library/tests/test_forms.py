from werkzeug.datastructures import MultiDict
from app import app, db

from library.forms import BookForm, AuthorForm, LoginForm

from ..models import User, Author

from . import TestCase

class BookFormTest(TestCase):
    def test_validation(self):
        data = MultiDict({
            'title': 'Book title'
        })
        a = Author(name='Nabokov')
        db.session.add(a)
        with app.app_context():
            f = BookForm(formdata=data)
            self.assertFalse(f.validate())

            data['authors-0'] = a.id
            f = BookForm(formdata=data)
            self.assertTrue(f.validate())


class LoginFormTest(TestCase):
    def test(self):
        u = User(email='email@mail.com', password='password')
        db.session.add(u)
        db.session.commit()
        with app.app_context():
            f = LoginForm(data={
                'email': u.email,
                'password': 'password'
            })
        self.assertTrue(f.validate())
        with app.app_context():
            f = LoginForm(data={
                'email': u.email,
                'password': 'pwd'
            })
        self.assertFalse(f.validate())
