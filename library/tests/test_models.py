from app import db

from . import TestCase
from ..models import Author, Book, User, book_author,\
     get_or_build, replace_authors, delete_book

class BookTest(TestCase):
    def test_unicode(self):
        b = Book(title='Test')
        self.assertEqual(unicode(b), u'Test')

    def test_replace_authors(self):
        b = Book(title='Test')
        b.authors.append(Author(name='1'))
        db.session.add(b)
        self.assertEqual(b.authors_query.count(), 1)

        a2, a3 = Author(name='2'), Author(name='3')
        db.session.add(a2)
        db.session.add(a3)
        db.session.flush()
        replace_authors(b, [a2, a3])
        # assert that
        self.assertEqual(b.authors_query.order_by('id').all(), [a2, a3])
        # assert that first author is still in the DB
        self.assertTrue(Author.query.filter_by(id=1).first())

    def test_delete_book(self):
        b = Book(title='Test')
        b.authors.append(Author(name='1'))
        db.session.add(b)
        self.assertIsNotNone(Book.query.get(1))
        self.assertEqual(db.session.query(book_author).count(), 1)
        delete_book(b.id)
        self.assertEqual(db.session.query(book_author).count(), 0)
        self.assertIsNone(Book.query.get(1))


class UserTest(TestCase):
    def test_check_password(self):
        u = User('email@mail.com', 'pwd')
        self.assertTrue(u.check_password('pwd'))
        self.assertFalse(u.check_password('ppwwdd'))


class AuthorTest(TestCase):
    def test_get_or_build(self):
        a = Author(name='Author')
        db.session.add(a)
        db.session.commit()
        a2 = get_or_build(Author, name='Author')
        self.assertEqual(a.id, a2.id)
        a3 = get_or_build(Author, name='Author3')
        self.assertIsNone(a3.id)

