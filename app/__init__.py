from flask import Flask, session, redirect, url_for, Response, request
from config import databasedevelopment, databasedeployment, Config
import psycopg2.extras, os
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = str(os.environ.get("FLASK_SECRET_KEY"))
jwt = JWTManager(app)

if str(os.environ.get("FLASK_ENV")) == "development":
    db = databasedevelopment()
else:
    db = databasedeployment()

cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

from app import routes