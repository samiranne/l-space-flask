from flask import flash, request, redirect, url_for, abort
from flask import render_template
from flask.ext.login import login_required, login_user, logout_user, \
    current_user
from app_factory import app, db, login_manager
from models import *
from forms import LoginForm, RegistrationForm
import google_books_service
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# @app.before_request
# def before_request():
#     pass


# @app.after_request
# def after_request(response):
#     return response


@app.route('/')
def home(name="default", test="default"):
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data,
                    display_name=form.display_name.data)
        add_to_database(user)
        login_user(user, remember=True)
        flash('Welcome, {0}!'.format(form.display_name.data),
              category='success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        login_user(user, remember=True)

        next = request.args.get('next')
        # WE ARE CURRRENTLY ASSUMING 'next' IS VALID. IF PERMISSIONS ARE ADDED
        # LATER, THEN WE SHOULD ADD ADDITIONAL VALIDATION

        return redirect(next or url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(message=u'You have logged out.',
          category='success')
    return render_template('index.html')


@app.route('/app', methods=['GET', 'POST'])
@login_required
def app_default():
    return render_template('app.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    pass  # TODO allow user to get or modify their settings.


### BOOKS ###


@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get("query")
    scope = request.args.get("scope")
    starting_index = request.args.get("starting_index")
    query_params = google_books_service.format_query_params(query, scope)
    logger.debug(query_params)
    books = []
    total_items = 0
    # TODO: don't display add buttons for books already owned
    # by current user.
    if query:
        books, total_items = google_books_service.search_books(query_params)
    return render_template('books/search.html', books=books, query=query,
                           scope=scope, starting_index=starting_index,
                           # ending_index=starting_index + len(books),
                           total_items=total_items)


@app.route('/books/add', methods=['POST'])
def add_book():
    book_params = {k: v for k, v in request.form.items()}
    book = db.session.query(Book).\
        filter_by(google_books_id=book_params['google_books_id']).\
        first()
    if book is None:
        book = Book(**book_params)
    current_user.books.append(book)
    # db.session.begin()
    db.session.commit()
    return 'ok'


### HOUSES ###


@app.route('/houses/', methods=['GET'])
def houses():
    # TODO for now, redisrect to Godric's house id page.
    houses = House.query.all()
    return render_template('houses/index.html', houses=houses)


@app.route('/houses/<int:house_id>', methods=['GET'])
def house(house_id=None):
    house_books = []
    if house_id is not None:
        house = House.get_house_by_id(house_id)
        house_books = house.get_all_books()
    return render_template('houses/id.html', house=house, books=house_books)


@app.route('/houses/<int:house_id>/members', methods=['GET'])
def house_members(house_id):
    house = House.get_house_by_id(house_id)
    house_members = house.members
    return render_template('houses/members.html', members=house_members)


@app.route('/houses/add', methods=['GET', 'POST'])
def add_house():
    if request.method == 'POST':
        # try:
        house_name = request.form['name']
        house = House(name=house_name)
        add_to_database(house)
        flash('Created a new house "%s"' % house_name, category='success')
        # except: # TODO what exceptions to catch here?
        #     flash('An error occurred', category='error')
    return render_template('houses/add.html')

### USERS ###


@app.route('/users/<user_id>', methods=['GET'])
def user(user_id):
    user = User.get_user_by_id(user_id)
    return render_template('users/id.html', user=user)


@app.route('/users/book_copies/<book_copy_id>', methods=['GET'])
def user_book_copy(book_copy_id):
    pass
    # TODO:
    #   Add a unique primary key for user_books table.
    #   Get a user_book entry by id, and return it.
    # return render_template('users/book_copy_id.html', book=book)


### HANDLERS ###

@login_manager.user_loader
def load_user(userid):
    return User.get_user_by_id(userid)


@login_manager.unauthorized_handler
def unauthorized():
    flash(message='You must be logged in to do that.', category='error')
    return 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


# # COMMENT THIS CODE OUT FOR PRODUCTION, OR DON'T DISPLAY THE ERROR
# @app.errorhandler(500)
# def page_not_found(error):
#     return render_template('internal_server_error.html', error=error), 500


def add_to_database(object):
    # db.session.begin()
    db.session.add(object)
    db.session.commit()


if __name__ == '__main__':
    print("DATABASE_URL: " + app.config['SQLALCHEMY_DATABASE_URI'])
    print("DEBUG: " + str(app.config['DEBUG']))
    app.run()
