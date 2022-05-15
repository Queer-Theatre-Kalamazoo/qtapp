from flask import Blueprint

# Create blueprint
bp_person = Blueprint("bp_person", __name__, static_folder="static", template_folder="templates", url_prefix="/person") # Create Blueprint

from . import views