from flask_login import UserMixin
from app_factory import db, bcrypt
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OwnedBookCopy(db.Model):
    __tablename__ = 'owned_book_copies'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                         primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False,
                        primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            nullable=True)

    owner = db.relationship("User", backref=db.backref("owned_book_copies"),
                            foreign_keys='OwnedBookCopy.owner_id')
    book = db.relationship("Book", backref=db.backref("owned_book_copies"),
                           foreign_keys='OwnedBookCopy.book_id')

    def __repr__(self):
        return "OwnedBookCopy({0}:{1},{2})".format(
            self.id, self.owner, self.book)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(255))
    display_name = db.Column(db.String(), unique=True, nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'),
                         nullable=False)

    house = db.relationship('House', foreign_keys='User.house_id',
                            backref=db.backref('users', lazy=True))

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()

    def __init__(self, email, password, display_name):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.display_name = display_name
        # for v1.0, set all houses to Godric's.
        self.house_id = House.query.first().id

    def __repr__(self):
        return 'User({0}:{1})'.format(self.id, self.display_name)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    google_books_id = db.Column(db.String(), index=True, unique=True,
                                nullable=False)
    title = db.Column(db.String(), nullable=False)
    authors = db.Column(db.String())
    thumbnail_link = db.Column(db.String())

    def __repr__(self):
        return 'Book({0}:{1})'.format(self.id, self.title)

    @staticmethod
    def get_all_books():
        return Book.query.order_by(Book.title).all()

    @staticmethod
    def get_from_google_books_id(google_books_id):
        '''
        Returns the Book matching the given google_book_id.
        If none exists, returns None.
        '''
        return Book.query.\
            filter_by(google_books_id=google_books_id).\
            first()

    @staticmethod
    def create(**book_params):
        '''
        Creates a new Book using the provided **book_params,
        and commits it to the db.
        :returns: The newly-created book
        '''
        book = Book(**book_params)
        db.session.add(book)
        db.session.commit()
        return book


class House(db.Model):
    __tablename__ = 'houses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "House({0}:{1})".format(self.id, self.name)

    @staticmethod
    def get_house_by_id(id):
        return House.query.get(id)

    def get_all_owned_books(self):
        result = []
        for user in self.users:
            result.extend(user.owned_book_copies)
        return result
