from flask_wtf import Form
from wtforms import StringField, IntegerField, FieldList, PasswordField, ValidationError, BooleanField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app import app, db

from .models import User, Author, Book


class AuthorForm(Form):
    name = StringField('Author\'s name', validators=[DataRequired()])
    action = StringField('Action')

    def __init__(self, *args, **kwargs):
        self.obj = kwargs.get('obj')
        super(AuthorForm, self).__init__(*args, **kwargs)

    def validate(self):
        if self.action.data == 'delete':
            if self.obj.books:
                self.action.errors =\
                    ["You cannot delete an author who has associated books"]
                return False
            return True

        return super(AuthorForm, self).validate()


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


class RegisterForm(Form):
    email = StringField('Email address', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=5, message='Password length should be at least 5 chars long')]
    )
    password2 = PasswordField('Repeat password', validators=[
        EqualTo('password1', 'Password fields must match')]
    )

    def validate_email(self, field):
        if db.session.query(db.exists().where(User.email == field.data))\
                .scalar():
            raise ValidationError("Email already in use")
