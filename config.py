import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://library:godrics@localhost/library_dev") #defaults to localhost
    SECRET_KEY = "d97a21fb8e3d2b329b9278d1b66285af" # use the following in terminal to generate: "cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 32"
    GOOGLE_BOOKS_API_KEY = "AIzaSyBYhBTKNfv4JAw_f1xSpBXJ5v2wXazr1sw"

class SiteConfig:
    # these config values are used in the templates (e.g. open graph, twitter)
    SITE_NAME = "Godric's Hollow Library"
    SITE_KEYWORDS = "library, rationalist"
    SITE_OWNER = "Chelsea Voss and Samira Nedungadi"

    SITE_IMAGE = "img/book_icon.png"
    SITE_IMAGE_WIDTH = 600
    SITE_IMAGE_HEIGHT = 315


class ProductionConfig(Config, SiteConfig):
    DEBUG = False
    #uncomment to include GTM script in html pages
    #GOOGLE_TAG_MANAGER_ID = "GTM-XXXXXX"


class DevelopmentConfig(Config, SiteConfig):
    SQLALCHEMY_ECHO = True #prints out the created queries to the terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://library:godrics@localhost/library_test")
    TESTING = True
    SQLALCHEMY_ECHO = False #prints out the created queries to the terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = True

