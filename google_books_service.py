import requests
import logging
from app_factory import app
from models import Book
import json

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def search_books(query):
    books = []
    response_body = {}
    payload = {"q": query, "key": app.config["GOOGLE_BOOKS_API_KEY"]}
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes", params=payload)
    if response.status_code == 200:
        response_body = response.json()
        for item in response_body["items"]:
            google_books_id = item["id"]
            volume_info = item["volumeInfo"]
            logger.debug(json.dumps(volume_info, sort_keys=True, indent=4))
            author_list = volume_info.get("authors")
            author_string = ", ".join(author_list) if author_list else None
            title = volume_info["title"]
            image_links = volume_info.get("imageLinks")
            thumbnail_link = image_links.get(
                'thumbnail') if image_links else None
            books.append(Book(title=title, google_books_id=google_books_id,
                              authors=author_string,
                              thumbnail_link=thumbnail_link))
        return books
    else:
        # todo what exception should be raised here?
        raise requests.ConnectionError(response.status_code)
