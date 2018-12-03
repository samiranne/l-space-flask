L-space
===

A distributed community library

One-time setup
---
Have Python 3 and pip3 (or whatever will install dependencies for your Python 3 installation).

Install virtualenv using pip3:
```
pip3 install virtualenv
```

Then navigate to the repo and set up your virtual environment using virtualenv: 
```
virtualenv .venv
source .venv/bin/activate # if using a Windows Command Line, run .venv/Scripts/activate instead
```

Verify that the virtual environment is active by checking that `(.venv)` is prepended to your bash prompt.

Now, install requirements:
```
pip3 install -r requirements.txt
```

One-time setup for database
---

Install Postgres 10. Once it's installed, run `psql`. (On Windows, you will first need to add C:\Program Files\PostgreSQL\10\scripts to your path, and then run the command `runpsql`). You will be prompted to enter a server, database, port and username. Use the defaults provided by the prompts. Then run:

```
create database library_dev;
create user library with superuser password 'godrics';
```

Verify that your database name ("library_dev"), username ("library"), and password ("godrics") match that specified in `SQLALCHEMY_DATABASE_URI` in `config.py`.

Now, navigate to the repo and set up the tables:

```
python manage.py db migrate # creates migration scripts for tables in models.py
python manage.py db ugrade # runs migration scripts
```

Every time you enter the directory
---

Run venv to create the virtual environment.

```
source .venv/bin/activate # if using a Windows Command Line, run .venv/Scripts/activate instead
```

Verify that the above command ran successfully by checking that `(.venv)` is prepended to your bash prompt.

When exiting the directory, run this command to exit the virtual environment:

```
deactivate
```

To run the app locally
---

```
heroku local
```

Or, run through python:

```
python app.py # On Windows, use py -3 app.py
```

To run the tests
---
TODO: run dev env database setup before these will pass

```
python3 -m unittest tests.test_app
```

To deploy 
---

First, make sure that you have the heroku app added as a git remote:

```
heroku git:remote -a l-space
```

Once it is set up, use the following command to push commits to heroku:

```
git push heroku master
```

To manage the production db
---

After committing all new migrations, run them on production:

```
heroku run python manage.py db upgrade
```

To connect to and query the production database, run:

```
heroku pg:psql
```

For either of the above commands, if you get the error `You do not have access to the app project.`, specify the project name (`l-space`) using the `-a` flag.


Note that there are alembic upgrade scripts in migrations/versions that applied these upgrades.


View error logs
---

```
heroku logs
```

https://dashboard.heroku.com/apps/rationalist-library/logs
