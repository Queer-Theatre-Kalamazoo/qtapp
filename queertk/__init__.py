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
from queertk.authentication.authentication import bp_authentication

# Register blueprints
app.register_blueprint(bp_admin, url_prefix = '/admin')
app.register_blueprint(bp_productions, url_prefix = '/prod')
app.register_blueprint(bp_authentication, url_prefix = '/auth')

# Database setup
db_conn_string = app.config["SQLALCHEMY_DATABASE_URI"] # Pull URI from config
engine = create_engine(db_conn_string) # Instantiate SQLAlchemy create_engine

import queertk.views
import queertk.models

from datetime import datetime

@app.template_filter()
def format_datetime(value):
    
    return value.strftime("%d %B, %Y")