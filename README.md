rationalist-library
===

Distributed library of the rationalist community

One-time setup
---

- Have Python 3
- Have pip3 (for Python 3) or pip or whatever will install dependencies for your Python 3 installation
- Install virtualenv

```
virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Every time you enter the directory
---

```
source .venv/bin/activate
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
