from flask import Blueprint

# Create blueprint
bp_qtapp = Blueprint("bp_qtapp", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/qtapp") # Create Blueprint

from . import views