# L-Space

## Template

https://github.com/heroku/heroku-django-template

## To get it to run locally

Run once:

```
virtualenv venv
source venv/bin/activate
pip3 install django
pip3 install django-heroku
pip3 install gunicorn
pip3 install psycopg2-binary
django-admin.py startproject --template=https://github.com/heroku/heroku-django-template/archive/master.zip --name=Procfile l_space
```

Run once per terminal session: `virtualenv venv`

Then:

```
heroku local
```
