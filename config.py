import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://localhost/example_site") #defaults to localhost
    SECRET_KEY = "d97a21fb8e3d2b329b9278d1b66285af" # use the following in terminal to generate: "cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 32"

class SiteConfig:
    # these config values are used in the templates (e.g. open graph, twitter)
    SITE_NAME = "Flask Template"
    SITE_DESCRIPTION = "This site is a flask template designed for postgres/heroku."
    SITE_KEYWORDS = "flask, postgres, heroku"
    SITE_OWNER = "SHANE KERCHEVAL"
    SITE_EMAIL = "shane.kercheval@yahoo.com"

    SITE_IMAGE = "img/logo.png"
    SITE_IMAGE_WIDTH = 600
    SITE_IMAGE_HEIGHT = 315

    SITE_TWITTER_USERNAME = "ShaneKercheval"
    SITE_GITHUB_USERNAME = "shane-kercheval"


class ProductionConfig(Config, SiteConfig):
    DEBUG = False
    #uncomment to include GTM script in html pages
    #GOOGLE_TAG_MANAGER_ID = "GTM-XXXXXX"


class DevelopmentConfig(Config, SiteConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True #prints out the created queries to the terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    TEST_DATABASE_STRING = "test.db"
    DEBUG = True
    SQLALCHEMY_ECHO = False #prints out the created queries to the terminal
    SQLALCHEMY_TRACK_MODIFICATIONS = True

