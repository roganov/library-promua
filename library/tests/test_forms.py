from werkzeug.datastructures import MultiDict
from app import app

from library.forms import BookForm, AuthorForm

from . import TestCase

class BookFormTest(TestCase):
    def test_validation(self):
        data = MultiDict({
            'title': 'Book title'
        })
        with app.app_context():
            f = BookForm(formdata=data)
            self.assertFalse(f.validate())

            data['author_ids-0'] = 1
            f = BookForm(formdata=data)
            self.assertTrue(f.validate())
