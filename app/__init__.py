try:
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    # from flask_httpauth import HTTPBasicAuth
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

app = Flask(__name__, static_url_path="/static")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///..\database\\users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

database = SQLAlchemy()
database.init_app(app)


# auth = HTTPBasicAuth()

from app import routes, error_handlers

__version__ = "1.0.0"