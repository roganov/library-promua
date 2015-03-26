from flask_wtf import Form
from wtforms import StringField, IntegerField, FormField, FieldList
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email


class AuthorForm(Form):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Author\'s name', validators=[DataRequired()])

class BookForm(Form):
    title = StringField('Book title', validators=[DataRequired()])
    author_ids = FieldList(IntegerField(validators=[DataRequired()]),
                           min_entries=1)