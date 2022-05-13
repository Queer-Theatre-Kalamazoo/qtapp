from flask import Flask
from sqlalchemy import create_engine
from flask_breadcrumbs import Breadcrumbs

# Flask object creation
app = Flask(__name__)

# Flask-Breadcrumbs instantiation
Breadcrumbs(app)

# Select and load config object dynamically based on the value of FLASK_ENV in .env
if app.config["ENV"] == "production":
    app.config.from_object("application.config.ProductionConfig")
else:
    app.config.from_object("application.config.DevelopmentConfig")

# Import blueprints so they can be registered
from application.blueprints.common.common import bp_common
from application.blueprints.admin.admin import bp_admin
# from application.blueprints.authentication.authentication import bp_authentication
from application.blueprints.qtapp.qtapp import bp_qtapp
from application.blueprints.production.production import bp_productions
from application.blueprints.artist.artist import bp_artist
from application.blueprints.post.post import bp_post

# Register blueprints
app.register_blueprint(bp_common)
app.register_blueprint(bp_admin, url_prefix = '/admin')
# app.register_blueprint(bp_authentication, url_prefix = '/auth')
app.register_blueprint(bp_qtapp, url_prefix = '/app')
app.register_blueprint(bp_productions, url_prefix = '/prod')
app.register_blueprint(bp_artist, url_prefix = '/artist')
app.register_blueprint(bp_post, url_prefix = '/post')

# Database setup
db_conn_string = app.config["SQLALCHEMY_DATABASE_URI"] # Pull URI from config
engine = create_engine(db_conn_string) # Instantiate SQLAlchemy create_engine

import application.views

@app.template_filter()
def format_datetime(value):
    return value.strftime("%a %b %d, %Y at %I:%M:%S %p")