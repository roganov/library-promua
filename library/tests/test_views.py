from flask import url_for
from app import app, db
from . import TestCase
from ..models import User, Author, Book

class AuthorizedEditTest(TestCase):
    def test_not_authorized_cannot_edit(self):
        u = User(email='mail@mail.com', password='password')
        db.session.add(u)
        self.login(u.email, 'password')
        r = self.app.get(url_for('add_book_view'))
        self.assertEqual(r.status_code, 404)

    def test_authorized_can_edit(self):
        u = User(email='mail@mail.com', password='password', can_edit=True)
        db.session.add(u)
        rl = self.login(u.email, 'password')
        r = self.app.get(url_for('add_book_view'))
        self.assertEqual(r.status_code, 200)
