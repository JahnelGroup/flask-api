# Flask API 

This repository demonstrates a solid foundation for building a protected API with Flask.

## References

* [The Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg.
* [Designing a RESTful API with Python and Flask](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask) by Miguel Grinberg.

## Setup Environment

Configure a virtual environment, activate it and then install the requirements.

```bash
$ virtualenv venv -p python3
$ . venv/bin/activate
$ pip install -r requirements.txt
```

Initialize and then migrate a local SQLite database, you should then see a local *app.db* file.  

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```

You can view the database with [DB Browser for SQLite](https://sqlitebrowser.org/) or IntelliJ also has a plugin.

## Running the app

### Add a user via Flask Shell

```bash
$ flask shell
>>> from werkzeug.security import generate_password_hash
>>> db.session.add(User(username='steven', email='steven@example.com', password=generate_password_hash('pass')))
>>> db.session.commit()
>>> exit()
```

### Run 

```bash
$ flask run
$ curl localhost:5000/api/users
{"users":[{"email":"steven@example.com","id":2,"username":"steven"}]}
```

# Questions

* What is a better way to convert SQLAlchemy results to JSON?
* Intelli sense? Click to follow method prototypes?