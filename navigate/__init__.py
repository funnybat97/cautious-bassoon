from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
username = 'navigator'
password = 'password'
database = 'navigate_db'
DB_PORT = '5432'
DB_HOST = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{DB_HOST}:{DB_PORT}/{database}"

db = SQLAlchemy(app)

from navigate import routers
from navigate import models
from navigate import insert_data
