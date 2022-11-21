try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///..\database\\database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database = SQLAlchemy(app)

from app import routes

__version__ = "0.0.1"