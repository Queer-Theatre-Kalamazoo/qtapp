from flask import Flask
from sqlalchemy import create_engine

# Flask object creation
app = Flask(__name__)

# Select and load config object dynamically based on the value of FLASK_ENV in .env
if app.config["ENV"] == "production":
    app.config.from_object("queertk.config.ProductionConfig")
else:
    app.config.from_object("queertk.config.DevelopmentConfig")

from queertk.admin.admin import bp_admin
from queertk.production.production import bp_productions
# from queertk.authentication.authentication import bp_authentication

# Register blueprints
app.register_blueprint(bp_admin)
app.register_blueprint(bp_productions)
# app.register_blueprint(bp_authentication)

# Database setup
db_conn_string = app.config["SQLALCHEMY_DATABASE_URI"] # Pull URI from config
engine = create_engine(db_conn_string) # Instantiate SQLAlchemy create_engine

import queertk.views
import queertk.models

