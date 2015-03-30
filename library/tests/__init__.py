import unittest
from flask import url_for

from app import app, db

from ..models import User

class TestCase(unittest.TestCase):
    # Testing DB is recreated for every test
    # Better to create the DB once and wrap every test in transaction
    # But for now, let it be
    def setUp(self):
        app.config.from_object('config.TestConfig')
        if not app.config.get('TESTING'):
            raise ValueError("Testing config is not set up correctly")
        self.app = app.test_client()
        self._ctx = app.test_request_context()
        self._ctx.push()
        db.create_all()

    def tearDown(self):
        self._ctx.pop()
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.app.post(url_for('login'), data={
            'email': email,
            'password': password
        })

    def login_as_super(self):
        u = User(email='mail@mail.com', password='password', can_edit=True)
        db.session.add(u)
        self.login(u.email, 'password')
        return u

    def logout(self):
        self.app.get(url_for('logout'))