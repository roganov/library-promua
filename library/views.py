import json

from flask import render_template, url_for, redirect, request, jsonify, flash
from flask.ext.login import login_user, logout_user, login_required
from werkzeug.exceptions import abort

from app import app, db

from .forms import LoginForm, BookForm, AuthorForm
from library.models import replace_authors, delete_book
from .models import find_books, find_authors, add_book, Author, Book
from .utils import can_edit_required


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember=form.remember.data)
        flash("Successfully logged in!", "success")
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))

@app.route("/books")
@login_required
def books_view():
    title = request.args.get('title', '').strip()
    author_name = request.args.get('author', '').strip()
    books = find_books(title, author_name).all()
    return render_template('books.html', books=books)

@app.route("/books/add", methods=['GET', 'POST'])
@can_edit_required
def add_book_view():
    form = BookForm()
    if form.validate_on_submit():
        title = form.title.data
        authors = form.authors.authors
        add_book(title, authors)
        db.session.commit()
        flash('The book was successfully added', 'success')
        return redirect(url_for('books_view'))
    else:
        return render_template('add-book.html', form=form)

@app.route("/books/<int:book_id>", methods=['GET', 'POST'])
@can_edit_required
def edit_book_view(book_id):
    obj = Book.query.options(db.joinedload(Book.authors)).get(book_id)
    if obj is None:
        abort(404)
    form = BookForm(obj=obj)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'save' and form.validate_on_submit():
            obj.title = form.title.data
            authors = form.authors.authors
            replace_authors(obj, authors)
            db.session.commit()
            flash('The book was successfully edited', 'success')
            return redirect(url_for('books_view'))
        elif action == 'delete':
            delete_book(book_id)
            db.session.commit()
            flash('The book was successfully deleted', 'success')
            return redirect(url_for('books_view'))
    return render_template('add-book.html', form=form, obj=obj)


@app.route("/api/authors/add", methods=['POST'])
@can_edit_required
def add_author_view():
    form = AuthorForm()
    if form.validate_on_submit():
        a = Author()
        form.populate_obj(a)
        db.session.add(a)
        db.session.commit()
        return jsonify(id=a.id, name=a.name)

@app.route("/api/authors")
@login_required
def authors_api():
    prefix = request.args.get('prefix')
    name = request.args.get('name')
    with_books = request.args.get('with_books') == '1'
    authors = Author.query
    if name:
        authors = authors.filter(Author.name == name)
    elif prefix:
        authors = authors.filter(Author.name.startswith(prefix))
    if with_books:
        authors = authors.options(db.joinedload(Author.books))
        data = [{'id': a.id, 'name': a.name,
                 'books': [b.title for b in a.books]}
                for a in authors]
    else:
        data = [{'id': a.id, 'name': a.title} for a in authors]
    return jsonify(result=data)

@app.route("/authors")
@login_required
def authors_view():
    title = request.args.get('title', '').strip()
    author_name = request.args.get('author', '').strip()
    authors = find_authors(author_name, title).all()
    return render_template('authors.html', authors=authors)
