from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

def get_or_build(model, **fields):
    instance = model.query.filter_by(**fields).first()
    if not instance:
        instance = model(**fields)
    return instance

book_author = db.Table('book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('author.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    authors = db.relationship('Author', secondary='book_author',
                              backref=db.backref('books', lazy='dynamic'),
                              lazy='dynamic')

    def __unicode__(self):
        return self.title


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __unicode__(self):
        return self.name

def replace_authors(book, author_ids):
    authors = Author.query.filter(Author.id.in_(author_ids)).all()
    book.authors = authors
    return book


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)