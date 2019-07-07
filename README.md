venv
pip install -r requirements.txt

Flask
flask-sqlalchemy
flask-migrate

elasticbeanstalk


# Migrate Database

$ flask db init
$ flask db migrate
$ flask db upgrade

# Add a user

$ flask shell
>>> from werkzeug.security import generate_password_hash
>>> db.session.add(User(username='steven', email='steven@example.com', password=generate_password_hash('pass')))
>>> db.session.commit()
>>> exit()

# View database

https://github.com/sqlitebrowser/sqlitebrowser
-or-
use intellij

# Run 

$ flask run


# Questions

SQLAlchemy results to JSON