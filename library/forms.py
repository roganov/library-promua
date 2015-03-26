from flask_wtf import Form
from wtforms import StringField, IntegerField, FieldList, PasswordField, ValidationError
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email

from .models import User


class AuthorForm(Form):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Author\'s name', validators=[DataRequired()])


class BookForm(Form):
    title = StringField('Book title', validators=[DataRequired()])
    author_ids = FieldList(IntegerField(validators=[DataRequired()]),
                           min_entries=1)

class LoginForm(Form):
    email = StringField('Email address', validators=[Email(), DataRequired()])
    password = PasswordField('Password')

    def validate_password(self, field):
        user = User.query.filter_by(
            email=self.email.data).first()
        if user is None or not user.check_password(field.data):
            raise ValidationError('Invalid email or password')
        self.user = user
