from flask import Blueprint

# Create Blueprint
bp_common = Blueprint("bp_common", __name__, static_folder = "static", template_folder = "templates")
