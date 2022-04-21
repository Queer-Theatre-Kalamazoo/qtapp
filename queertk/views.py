from queertk import app
# from flask import Blueprint

# app_views = Blueprint("app_views", __name__, static_folder = "static", template_folder = "templates") # Create Blueprint

@app.route('/')
def home():
    return "Hello"