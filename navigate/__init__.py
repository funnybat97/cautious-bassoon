from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
username = 'navigator'
password = 'password'
database = 'navigate_db'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{database}"
db = SQLAlchemy(app)

from navigate import routers
from navigate import models

if __name__ == '__main__':
    app.run(port=5000, debug = True)