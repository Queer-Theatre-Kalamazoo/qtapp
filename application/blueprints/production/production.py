from flask import Blueprint

# Create blueprint
bp_productions = Blueprint(
    "productions",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/prod",
)  # Create Blueprint

from . import views
