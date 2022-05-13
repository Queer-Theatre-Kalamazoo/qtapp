from flask import Blueprint, render_template, url_for

# Create blueprint
bp_artist = Blueprint("artists", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/artist") # Create Blueprint

from . import views