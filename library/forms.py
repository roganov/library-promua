from flask_wtf import Form
from wtforms import StringField, IntegerField, FieldList, PasswordField, ValidationError, BooleanField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email

from .models import User, Author


class AuthorForm(Form):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Author\'s name', validators=[DataRequired()])


class BookForm(Form):
    title = StringField('Book title', validators=[DataRequired()])
    authors = FieldList(IntegerField(validators=[DataRequired()]),
                           min_entries=1)

    def validate_authors(self, field):
        ids = field.data
        authors = Author.query.filter(Author.id.in_(ids)).all()
        if not authors:
            field.errors = []
            raise ValidationError("At least one author is required")
        field.authors = authors

class LoginForm(Form):
    email = StringField('Email address', validators=[Email(), DataRequired()])
    password = PasswordField('Password')
    remember = BooleanField('Remember', default=False)

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None or not user.check_password(field.data):
            raise ValidationError('Invalid email or password')
        self.user = user
