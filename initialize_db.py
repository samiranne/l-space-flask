from models import *
from app_factory import db


def add_to_database(object):
    db.session.add(object)
    db.session.commit()


db.session.close()
db.drop_all()
db.create_all()

add_to_database(User(email='test_email', password='test_password'))
add_to_database(User(email='test@gmail.com', password='shane_password'))

author = Author(name='Neil Gaiman')
add_to_database(author)
add_to_database(Book(title='Coraline', google_books_id='QSuPPwAACAAJ',
    authors=[author]))
