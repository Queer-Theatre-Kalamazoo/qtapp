from flask import Flask
from sqlalchemy import create_engine
from flask_breadcrumbs import Breadcrumbs
from flask_ckeditor import CKEditor

def init_app():
    # Initialize the core application
    app = Flask(__name__, instance_relative_config=True)

    # Select and load config object dynamically based on the value of FLASK_ENV in .env
    if app.config["ENV"] == "production":
        app.config.from_object("application.config.ProductionConfig")
    else:
        app.config.from_object("application.config.DevelopmentConfig")

    # Flask-Breadcrumbs instantiation
    Breadcrumbs(app)
    ckeditor = CKEditor(app)


    with app.app_context():
        from application.blueprints.common import bp_common
        # from application.blueprints.admin import bp_admin
        from application.blueprints.management import bp_management
        from application.blueprints.production import bp_production
        from application.blueprints.artist import bp_artist
        from application.blueprints.post import bp_post

        app.register_blueprint(bp_common)
        # app.register_blueprint(bp_admin, url_prefix = '/admin')
        app.register_blueprint(bp_management, url_prefix = '/app')
        app.register_blueprint(bp_production, url_prefix = '/production')
        app.register_blueprint(bp_artist, url_prefix = '/artist')
        app.register_blueprint(bp_post, url_prefix = '/post')

        @app.template_filter()
        def format_datetime(value):
            return value.strftime("%a %b %d, %Y at %I:%M:%S %p")

        import application.views

        return app

app = init_app()