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
        b = self.make_book()
        r = self.app.get(url_for('edit_book_view', book_id=b.id))
        self.assertEqual(r.status_code, 404)

    def test_authorized_can_edit(self):
        u = self.login_as_super()
        r = self.app.get(url_for('add_book_view'))
        self.assertEqual(r.status_code, 200)
        b = make_book()
        r = self.app.get(url_for('edit_book_view', book_id=b.id))
        self.assertEqual(r.status_code, 200)

def make_book():
    b = Book(title='Book')
    b.authors.append(Author(name='Author'))
    db.session.add(b)
    db.session.flush()
    return b

class EditBookTest(TestCase):
    def test_delete(self):
        bid = make_book().id
        u = self.login_as_super()
        self.app.post(url_for('edit_book_view', book_id=bid), data={
            'action': 'delete'
        })
        self.assertIsNone(Book.query.get(bid))
