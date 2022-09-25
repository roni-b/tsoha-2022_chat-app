from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
#tee env

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
db = SQLAlchemy(app)

