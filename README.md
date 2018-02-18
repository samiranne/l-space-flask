rationalist-library
===

Distributed library of the rationalist community

One-time setup
---

- Have Python 3
- Have pip3 (for Python 3) or pip or whatever will install dependencies for your Python 3 installation
- Install virtualenv

```
pip3 install virtualenv
virtualenv .venv
source .venv/bin/activate # if using a Windows Command Line, just run .venv/Scripts/activate
pip3 install -r requirements.txt
```

Every time you enter the directory
---

Run venv to create the virtual environment.

```
source .venv/bin/activate # if using a Windows Command Line, just run .venv/Scripts/activate
```

Verify that the above command ran successfully by checking that `(.venv)` is prepended to your bash prompt.

When exiting the directory, run this command to exit the virtual environment:

```
deactivate
```

To run the app locally
---
TODO: add instructions for how to set up local postgres here, so that you can test creating users etc

```
heroku local
```

To run the tests
---
TODO: run dev env database setup before these will pass

```
python3 -m unittest tests.test_app
```

To deploy (one-time setup)
---

```
heroku git:remote -a rationalist-library
```

To deploy (each time)
---

```
git push heroku master
```


To manage the db
---
```
heroku run "python manage.py db --help"
```

To create the Users table in the prod db, I had to run:
```
heroku run "python manage.py db upgrade"
```

I expect we'll have to run this after adding any new db models. Note that there
are alembic upgrade files in migrations/versions that applied these upgrades.
