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
        b = make_book()
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


class AddAuthorTest(TestCase):
    def test(self):
        self.login_as_super()
        r = self.app.post(url_for('add_author_view'), data={
            'name': 'Jane Doe',
        })
        self.assertEqual(Author.query.count(), 1)



class EditAuthorTest(TestCase):
    def test_edit(self):
        a = Author(name='John Doe')
        db.session.add(a)
        db.session.flush()
        self.login_as_super()
        self.app.post(url_for('edit_author_view', author_id=a.id), data={
            'name': 'Jane Doe',
            'action': 'save'
        })
        self.assertEqual(a.name, 'Jane Doe')

    def test_delete(self):
        a = Author(name='John Doe')
        db.session.add(a)
        db.session.flush()
        self.assertEqual(Author.query.all(), [a])
        self.login_as_super()
        self.app.post(url_for('edit_author_view', author_id=a.id), data={
            'action': 'delete'
        })
        self.assertEqual(Author.query.all(), [])
