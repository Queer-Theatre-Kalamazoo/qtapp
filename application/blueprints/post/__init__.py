from flask import Blueprint, render_template

# Create Blueprint
bp_post = Blueprint(
    "bp_post",
    __name__,
    static_folder="static",
    template_folder="templates"
)

from . import views
