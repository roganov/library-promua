from werkzeug.datastructures import MultiDict
from app import app

from library.forms import BookForm, AuthorForm

from . import TestCase

class BookFormTest(TestCase):
    def test_validation(self):
        data = MultiDict({
            'title': 'Book title',
        })
        with app.app_context():
            f = BookForm(formdata=data)
            self.assertFalse(f.validate())

            data['authors-0-name'] = 'Author'
            f = BookForm(formdata=data)
            self.assertTrue(f.validate())

    def test_get_obj(self):
        data = MultiDict({
            'title': 'Book title',
            'authors-0-name': 'Author'
            })
        with app.app_context():
            f = BookForm(formdata=data)
        book = f.get_obj()
        self.assertEqual(book.authors.first().name, 'Author')
        self.assertEqual(book.authors.count(), 1)

