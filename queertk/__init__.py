from flask import Flask
from sqlalchemy import create_engine

# Flask object creation
app = Flask(__name__)

# Select and load config object dynamically based on the value of FLASK_ENV in .env
if app.config["ENV"] == "production":
    app.config.from_object("queertk.config.ProductionConfig")
else:
    app.config.from_object("queertk.config.DevelopmentConfig")

# Import blueprints so they can be registered
from queertk.blueprints.common.common import bp_common
from queertk.blueprints.admin.admin import bp_admin
from queertk.blueprints.authentication.authentication import bp_authentication
from queertk.blueprints.production.production import bp_productions
from queertk.blueprints.artist.artist import bp_artist
from queertk.blueprints.post.post import bp_post

# Register blueprints
app.register_blueprint(bp_common)
app.register_blueprint(bp_admin, url_prefix = '/admin')
app.register_blueprint(bp_authentication, url_prefix = '/auth')
app.register_blueprint(bp_productions, url_prefix = '/prod')
app.register_blueprint(bp_artist, url_prefix = '/artist')
app.register_blueprint(bp_post, url_prefix = '/post')

# Database setup
db_conn_string = app.config["SQLALCHEMY_DATABASE_URI"] # Pull URI from config
engine = create_engine(db_conn_string) # Instantiate SQLAlchemy create_engine

import queertk.views

@app.template_filter()
def format_datetime(value):
    return value.strftime("%a %b %d, %Y at %I:%M:%S %p")