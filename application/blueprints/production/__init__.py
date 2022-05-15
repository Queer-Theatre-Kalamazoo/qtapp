from flask import Blueprint

# Create blueprint
bp_production = Blueprint(
    "bp_production",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/production",
)  # Create Blueprint

from . import views
