import os
import psycopg2
import psycopg2.extras

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET_KEY"))
    UPLOAD_FOLDER = str(os.environ.get("UPLOAD_FOLDER"))
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

def databasedevelopment():
    HOST = str(os.environ.get("DB_DEVELOPMENT_HOST"))
    PORT = str(os.environ.get("DB_DEVELOPMENT_PORT"))
    DATABASE = str(os.environ.get("DB_DEVELOPMENT_DATABASE"))
    USERNAME = str(os.environ.get("DB_DEVELOPMENT_USERNAME"))
    PASSWORD = str(os.environ.get("DB_DEVELOPMENT_PASSWORD"))
    database = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USERNAME, password=PASSWORD)
    return database

def databasedeployment():
    # HOST = str(os.environ.get("DB_DEPLOYMENT_HOST"))
    # PORT = str(os.environ.get("DB_DEPLOYMENT_PORT"))
    # DATABASE = str(os.environ.get("DB_DEPLOYMENT_DATABASE"))
    # USERNAME = str(os.environ.get("DB_DEPLOYMENT_USERNAME"))
    # PASSWORD = str(os.environ.get("DB_DEPLOYMENT_PASSWORD"))
    database = psycopg2.connect(host="ec2-34-197-249-102.compute-1.amazonaws.com", port="5432", database="d1a4p6afnvq0n1", user="tkgacmzsgqhkqz", password="e59a0a1233e24111e17458b333c0bb512eb3ffd0d6e62576fca8f1f40ef5d8b5")
    return database
