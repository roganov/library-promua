from flask import url_for
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


book_author = db.Table('book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('author.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    authors = db.relationship('Author', secondary='book_author',
                              backref=db.backref('books'))
    authors_query = db.relationship('Author', secondary='book_author',
                                    backref=db.backref('books_query', lazy='dynamic'),
                                    lazy='dynamic')

    def get_url(self):
        return url_for('edit_book_view', book_id=self.id)

    def __unicode__(self):
        return self.title


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def get_url(self):
        return url_for('edit_author_view', author_id=self.id)

    def __unicode__(self):
        return self.name


def replace_authors(book, authors):
    book.authors = authors
    db.session.add(book)
    return book


def add_book(title, authors):
    book = Book(title=title)
    replace_authors(book, authors)
    db.session.add(book)
    return book


def delete_book(book_id):
    del_stm = book_author.delete().where(book_author.c.book_id == book_id)
    db.session.execute(del_stm)
    Book.query.filter_by(id=book_id).delete()


def contains(term):
    return '%{}%'.format(term)


def find_books(title, author_name):
    res = Book.query.order_by(Book.title)
    if title:
        res = res.filter(Book.title.ilike(contains(title)))
    if author_name:
        res = res.filter(Book.authors.any(Author.name.ilike(contains(author_name))))
    return res.options(db.joinedload(Book.authors))


def find_authors(author_name, title):
    res = Author.query.order_by(Author.name)
    if author_name:
        res = res.filter(Author.name.ilike(contains(author_name)))
    if title:
        res = res.filter(Author.books.any(Book.title.ilike(contains(title))))
    return res.options(db.joinedload(Author.books))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    can_edit = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, can_edit=False):
        self.email = email
        self.set_password(password)
        self.can_edit = can_edit

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))