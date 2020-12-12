import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'papernest-secret-key'
    # PostgreSQL DB Path. The DB should have the POSTGIS extension for geographic coordinates.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://postgres:password@localhost:5433'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOUV_API_ADDRESS = os.environ.get('GOUV_API_ADDRESS') or "https://api-adresse.data.gouv.fr/search/"
