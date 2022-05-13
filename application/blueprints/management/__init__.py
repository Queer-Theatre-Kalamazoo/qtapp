from flask import Blueprint

# Create blueprint
bp_management = Blueprint(
    "bp_management",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/management",
)  # Create Blueprint

from . import views
