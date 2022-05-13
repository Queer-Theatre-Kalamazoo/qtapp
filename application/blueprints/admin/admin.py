from flask import Blueprint, render_template

# Create Blueprint
bp_admin = Blueprint("bp_admin", __name__, static_folder = "static", template_folder = "templates")

from flask_admin import Admin
from application import app

# Initialize database and Admin
admin = Admin(app)

from . import views





