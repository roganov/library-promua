from werkzeug.datastructures import MultiDict
from app import app, db

from library.forms import BookForm, AuthorForm, LoginForm, RegisterForm

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
        f = LoginForm(data={
            'email': u.email,
            'password': 'password'
        })
        self.assertTrue(f.validate())
        f = LoginForm(data={
            'email': u.email,
            'password': 'pwd'
        })
        self.assertFalse(f.validate())

class RegisterFormTest(TestCase):
    def test_ok(self):
        f = RegisterForm(data={
            'email': 'test@mail.com',
            'password1': '111111',
            'password2': '111111'
        })
        self.assertTrue(f.validate())

    def test_used_email(self):
        u = User(email='test@mail.com', password='password')
        db.session.add(u)
        f = RegisterForm(data={
            'email': 'test@mail.com',
            'password1': '111111',
            'password2': '111111'
        })
        self.assertFalse(f.validate())

    def test_pwd_mismatch(self):
        f = RegisterForm(data={
            'email': 'test@mail.com',
            'password1': '111111',
            'password2': '11111'
        })
        self.assertFalse(f.validate())

    def test_short_pwd(self):
        f = RegisterForm(data={
            'email': 'test@mail.com',
            'password1': '1111',
            'password2': '1111'
        })
        self.assertFalse(f.validate())
