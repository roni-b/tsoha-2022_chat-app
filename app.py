from flask import Flask
from os import getenv

app = Flask(__name__)

#app.secret_key = getenv("SECRET_KEY")
app.secret_key = "28c3d325dddb0c6b63069c300aece32f"
from db import db
import routes
