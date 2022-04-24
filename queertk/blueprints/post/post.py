from flask import Blueprint, render_template

# Create Blueprint
bp_post = Blueprint("bp_post", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/post")

from . import views