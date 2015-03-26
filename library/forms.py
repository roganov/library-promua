from flask_wtf import Form
from wtforms import StringField, IntegerField, FormField, FieldList
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email

from .models import get_or_build, Book, Author

class AuthorForm(Form):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Author\'s name', validators=[DataRequired()])

class BookForm(Form):
    title = StringField('Book title', validators=[DataRequired()])
    authors = FieldList(FormField(AuthorForm), min_entries=1)

    def get_obj(self):
        obj = Book(title=self.title.data)
        for author_f in self.authors.entries:
            if not author_f.data['id']:
                author = get_or_build(Author, name=author_f.data['name'])
                obj.authors.append(author)
        return obj