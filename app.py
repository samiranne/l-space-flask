import json
import logging

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

import google_books_service
from app_factory import app, login_manager
from forms import LoginForm, RegistrationForm, UpdateUserAccountForm
from models import *

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route("/")
def home():
    house = House.query.first()
    # For v1.0, redirect to the landing page for the default house
    if house:
        return redirect(url_for("house", house_id=house.id))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User(
            email=form.email.data, password=form.password.data, display_name=form.display_name.data
        )
        add_to_database(user)
        login_user(user, remember=True)
        flash("Welcome, {0}!".format(form.display_name.data), category="success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        login_user(user, remember=True)
        next = request.args.get("next")
        return redirect(next or url_for("home"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash(message="You have logged out.", category="success")
    return render_template("index.html")


@app.route("/app", methods=["GET", "POST"])
@login_required
def app_default():
    return render_template("app.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = UpdateUserAccountForm(current_user, request.form)
    if request.method == "POST" and form.validate_on_submit():
        current_user.email = form.email.data
        current_user.display_name = form.display_name.data
        if not current_user.check_password(
            form.new_password.data
        ):  # if new password != current password
            current_user.set_password(form.new_password.data)
        add_to_database(current_user)
        flash("Your changes have been saved", "success")
    elif request.method == "GET":
        form.pre_populate()  # pre-populate with the user's current display name, etc
    houses = House.query.all()
    house_membership = HouseMembership.query.filter_by(user_id=current_user.id).first()
    house = (
        House.query.filter_by(id=house_membership.house_id).first() if house_membership else None
    )
    return render_template("settings.html", user_account_form=form, house=house, houses=houses)


@app.route("/house_membership_requests", methods=["POST"])
@login_required
def house_membership_requests():
    request_body = {k: v for k, v in request.form.items()}
    membership_request = HouseMembershipRequests(
        house_id=request_body["house_id"], user_id=current_user.id
    )
    add_to_database(membership_request)
    return json.dumps({"requestId": membership_request.id})


@app.route("/house_membership_requests", methods=["GET"])
@login_required
def get_house_membership_requests():
    current_house_membership = HouseMembership.query.filter_by(user_id=current_user.id).first()
    if current_house_membership.is_admin:
        membership_requests = current_house_membership.house.house_membership_requests
        template = "houses/membership_requests.html" if request.is_xhr else "admin_settings.html"
        return render_template(template, membership_requests=membership_requests)
    else:
        flash(message="You must be the admin of a house to do that.", category="error")
        return 403


@app.route("/house_membership_requests/<int:request_id>", methods=["DELETE"])
@login_required
def delete_house_membership_request(request_id):
    membership_request = HouseMembershipRequests.query.filter_by(id=request_id).first()
    if membership_request:
        delete_from_database(membership_request)
        if membership_request.user != current_user:  # Admin rejecting someone else's request
            flash("Successfully rejected.")
    return "ok"


@app.route("/house_memberships", methods=["POST"])
@login_required
def add_house_membership_from_membership_request():
    logger.debug({k: v for k, v in request.form.items()})
    membership_request_dict = {k: v for k, v in request.form.items()}
    user_id, house_id = membership_request_dict["user_id"], membership_request_dict["house_id"]
    membership_request = HouseMembershipRequests.query.filter_by(
        house_id=house_id, user_id=user_id
    ).first()
    existing_house_membership = HouseMembership.query.filter_by(user_id=user_id).first()
    if existing_house_membership:
        logger.debug(
            f"User {user_id} was already found to be in house {existing_house_membership.house_id};"
            + " deleting existing relation"
        )
        delete_from_database(existing_house_membership)
    new_house_membership = HouseMembership(house_id=house_id, user_id=user_id)
    add_to_database(new_house_membership)
    delete_from_database(membership_request)
    return "ok"


# BOOKS


@app.route("/books/search", methods=["GET"])
@login_required
def search_books():
    query = request.args.get("query")
    scope = request.args.get("scope")
    starting_index = request.args.get("starting_index")
    query_params = google_books_service.format_query_params(query, scope)
    books = []
    total_items = 0
    owned_google_book_ids = [
        book_copy.book.google_books_id for book_copy in current_user.owned_book_copies
    ]
    if query:
        books, total_items = google_books_service.search_books(query_params)
    books = google_books_service.clean_up_results(books, owned_google_book_ids)
    return render_template(
        "books/search.html",
        books=books,
        query=query,
        scope=scope,
        starting_index=starting_index,
        # ending_index=starting_index + len(books),
        total_items=total_items,
        owned_google_book_ids=owned_google_book_ids,
    )


@app.route("/owned_book_copies", methods=["POST"])
@login_required
def create_owned_book_copy():
    book_params = {k: v for k, v in request.form.items()}
    book = Book.get_from_google_books_id(book_params["google_books_id"])
    if book is None:
        book = Book.create(**book_params)
    owned_copy = OwnedBookCopy(owner_id=current_user.id, book_id=book.id)
    add_to_database(owned_copy)
    return "ok"


@app.route("/owned_book_copies/<int:owned_book_copy_id>", methods=["DELETE"])
@login_required
def delete_owned_book_copy(owned_book_copy_id):
    owned_book_copy = OwnedBookCopy.get_owned_book_copy_by_id(id=owned_book_copy_id)
    if owned_book_copy:
        delete_from_database(owned_book_copy)
    return "ok"


# HOUSES


@app.route("/houses", methods=["GET"])
def houses():
    # TODO for now, redirect to Godric's house id page.
    houses = House.query.all()
    return render_template("houses/index.html", houses=houses)


@app.route("/houses/<int:house_id>", methods=["GET"])
def house(house_id=None):
    house = House.get_house_by_id(house_id)
    if house is None:
        return page_not_found()
    search_string = request.args.get("query")
    if search_string is not None:
        owned_book_copies = OwnedBookCopy.get_by_house(
            house, book_search_string=search_string
        ).all()
    else:
        owned_book_copies = OwnedBookCopy.get_by_house(house)
    return render_template("houses/id.html", house=house, owned_book_copies=owned_book_copies)


@app.route("/houses/<int:house_id>/members", methods=["GET"])
def house_members(house_id):
    house = House.get_house_by_id(house_id)
    if house is None:
        return page_not_found()
    house_members = house.members
    return render_template("houses/members.html", members=house_members)


@app.route("/houses", methods=["POST"])
def add_house():
    # try:
    house_name = request.form["name"]
    house = House(name=house_name)
    add_to_database(house)
    flash('Created a new house "%s"' % house_name, category="success")
    # except: # TODO what exceptions to catch here?
    #     flash('An error occurred', category='error')
    return "ok"


# USERS


@app.route("/users/<user_id>", methods=["GET"])
def user(user_id):
    user = User.get_user_by_id(user_id)
    if user is None:
        return page_not_found()
    return render_template("users/id.html", user=user, owned_book_copies=user.owned_book_copies)


# HANDLERS


@login_manager.user_loader
def load_user(userid):
    return User.get_user_by_id(userid)


@login_manager.unauthorized_handler
def unauthorized():
    flash(message="You must be logged in to do that.", category="error")
    return 200


@app.errorhandler(404)
def page_not_found(error=None):
    return render_template("page_not_found.html"), 404


# # COMMENT THIS CODE OUT FOR PRODUCTION, OR DON'T DISPLAY THE ERROR
# @app.errorhandler(500)
# def page_not_found(error):
#     return render_template('internal_server_error.html', error=error), 500


def add_to_database(object):
    db.session.add(object)
    db.session.commit()


def delete_from_database(object):
    db.session.delete(object)
    db.session.commit()


if __name__ == "__main__":
    print("DATABASE_URL: " + app.config["SQLALCHEMY_DATABASE_URI"])
    print("DEBUG: " + str(app.config["DEBUG"]))
    app.run()
