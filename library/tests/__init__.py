import unittest
from flask import url_for

from app import app, db

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
        with app.app_context():
            self.app.post(url_for('login'), {
                'email': email,
                'password': password
            })

    def logout(self):
        with app.app_context():
            self.app.get(url_for('logout'))