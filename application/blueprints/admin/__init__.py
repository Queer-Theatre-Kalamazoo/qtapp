from flask import Blueprint

# Create Blueprint
bp_admin = Blueprint("bp_admin", __name__, static_folder = "static", template_folder = "templates")

# from flask_admin import Admin
# from flask import Flask

# app = Flask(__name__)
# admin = Admin(app)

from . import views





