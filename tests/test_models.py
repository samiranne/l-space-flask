import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, House, OwnedBookCopy, User


class TestModels(unittest.TestCase):
    def add_to_database(self, object):
        self.session.add(object)
        self.session.commit()

    def create_user(self):
        user = User(display_name="test_user", email="test@email.com", password="test_password")
        self.add_to_database(user)
        return user

    def create_book(self, title="test_title", google_books_id="1", authors="test_authors"):
        book = Book(title=title, google_books_id=google_books_id, authors=authors)
        self.add_to_database(book)
        return book

    def create_owned_book_copy(self, owner=None, book=None):
        if book is None:
            book = self.create_book()
        if owner is None:
            owner = self.create_user()
        owned_book = OwnedBookCopy(owner=owner, book=book)
        self.add_to_database(owned_book)

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        User.metadata.create_all(self.engine)
        Book.metadata.create_all(self.engine)
        House.metadata.create_all(self.engine)
        OwnedBookCopy.metadata.create_all(self.engine)
        self.user = self.create_user()
        self.book = self.create_book(
            title="Title One", google_books_id="1", authors="First Author"
        )
        self.another_book = self.create_book(
            title="Title Two", google_books_id="2", authors="Second Author"
        )
        self.owned_book_copy = self.create_owned_book_copy(self.user, self.book)
        self.another_owned_book_copy = self.create_owned_book_copy(self.user, self.another_book)

    def tearDown(self):
        User.metadata.drop_all(self.engine)
        Book.metadata.drop_all(self.engine)
        House.metadata.drop_all(self.engine)
        OwnedBookCopy.metadata.drop_all(self.engine)
        self.session.close()

    def test_user_created_successfully(self):
        user_by_name = (
            self.session.query(User).filter_by(display_name=self.user.display_name).first()
        )
        self.assertIsNotNone(user_by_name)

    def test_get_owned_book_copy_by_user(self):
        copies = OwnedBookCopy.get_by_owner(owner=self.user).all()
        self.assertEqual(len(copies), 2)
        self.assertEqual(copies[0].google_books_id, self.book.google_books_id)

    def test_get_owned_book_copy_by_title_and_author(self):
        books_by_title = OwnedBookCopy.get_by_owner(
            owner=self.user, book_search_string="one"
        ).all()
        self.assertEquals(len(books_by_title), 1)
        self.assertEquals(books_by_title[0].book.authors, "First Author")
        books_by_author = OwnedBookCopy.get_by_owner(
            owner=self.user, book_search_string="author"
        ).all()
        self.assertEquals(len(books_by_author), 2)
