from flask import Blueprint, render_template

# Create Blueprint
bp_admin = Blueprint("bp_admin", __name__, static_folder = "static", template_folder = "templates")

from flask_admin import Admin
from queertk import app
from database import db

# Initialize database and Admin
admin = Admin(app)
db.init_app(app)

from . import views





