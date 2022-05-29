from flask import Blueprint

# Create blueprint
bp_person = Blueprint("bp_person", __name__, static_folder="static", static_url_path="/person/static", template_folder="templates") # Create Blueprint

from . import views