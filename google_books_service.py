import requests
import logging
from app_factory import app
from models import Book
# import json

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def format_query_params(query, scope=None):
    if scope is None or scope == "":
        return query
    else:
        return "{0}:{1}".format(scope, query)


def clean_up_results(query_results, owned_book_google_ids):
    '''
    Google Books' database contains duplicates (multiple results with
    the same title and author, but different ISBNs and Google Book IDs).
    We want to filter out these duplicates, but make sure we show the versions
    that are owned by the current user.
    '''
    logger.debug("Cleaning up results")
    title_author_to_book_mapping = {}
    for book in query_results:
        title_author = f"{book.title}_{book.authors}"
        if title_author in title_author_to_book_mapping:
            # We've seen this book already. So, skip it, unless
            # this version of the book is the version that the user
            # owns, in which case replace the other version with
            # this one.
            if book.google_books_id in owned_book_google_ids:
                title_author_to_book_mapping[title_author] = book
            else:
                logger.debug(
                    f"Skipping book {title_author} because it is a duplicate")
        else:
            title_author_to_book_mapping[title_author] = book
    return title_author_to_book_mapping.values()


def search_books(query_params):
    books = []
    total_items = 0
    response_body = {}
    payload = {
        "q": query_params,
        "key": app.config["GOOGLE_BOOKS_API_KEY"],
        "printType": "books"
    }
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes", params=payload)
    if response.status_code == 200:
        response_body = response.json()
        total_items = response_body["totalItems"]
        if total_items > 0:
            for item in response_body["items"]:
                google_books_id = item["id"]
                volume_info = item["volumeInfo"]
                # logger.debug(json.dumps(volume_info, sort_keys=True, indent=4))
                author_list = volume_info.get("authors")
                author_string = ", ".join(author_list) if author_list else None
                title = volume_info["title"]
                image_links = volume_info.get("imageLinks")
                thumbnail_link = image_links.get(
                    'thumbnail') if image_links else None
                book = Book(title=title, google_books_id=google_books_id,
                            authors=author_string,
                            thumbnail_link=thumbnail_link)
                books.append(book)
        return books, total_items
    else:
        # todo what exception should be raised here?
        raise requests.ConnectionError(response.status_code)
