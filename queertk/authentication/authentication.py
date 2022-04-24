from flask import Blueprint
from flask_login import LoginManager


# Create blueprint
bp_authentication = Blueprint("authentication", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/auth") # Create Blueprint

# Create LoginManager
login_manager = LoginManager()

from queertk import app

# Instatiate Flask-Admin app
login_manager.init_app(app)

# Load auth views
from . import views