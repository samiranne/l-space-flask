from flask.ext.login import UserMixin
from app_factory import db, bcrypt

# Refer to flask documentation on models:
# http://flask-sqlalchemy.pocoo.org/2.3/models/


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.LargeBinary(255))

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter_by(id=id).first()

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<USER:email- {}>'.format(self.email)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


book_authors = db.Table('book_authors', db.Model.metadata,
                        db.Column('book_id', db.Integer, db.ForeignKey(
                            'books.id'), primary_key=True),
                        db.Column('author_id', db.Integer, db.ForeignKey(
                            'authors.id'), primary_key=True)
                        )


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    google_books_id = db.Column(db.String(), unique=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    authors = db.relationship('Author', secondary=book_authors, lazy=True,
                              backref=db.backref('books', lazy=True)
                              )
    # TODO add from Google API: image_link, categories

    def __repr__(self):
        return 'Book({})'.format(self.title)

    @staticmethod
    def get_all_books():
        return Book.query.order_by(Book.title).all()


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
