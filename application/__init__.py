from flask import Flask
from sqlalchemy import create_engine
from flask_breadcrumbs import Breadcrumbs

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


    with app.app_context():
        from application.blueprints.common import bp_common
        from application.blueprints.admin import bp_admin
        from application.blueprints.qtapp import bp_qtapp
        from application.blueprints.production import bp_productions
        from application.blueprints.artist import bp_artist
        from application.blueprints.post import bp_post

        app.register_blueprint(bp_common)
        app.register_blueprint(bp_admin, url_prefix = '/admin')
        app.register_blueprint(bp_qtapp, url_prefix = '/app')
        app.register_blueprint(bp_productions, url_prefix = '/prod')
        app.register_blueprint(bp_artist, url_prefix = '/artist')
        app.register_blueprint(bp_post, url_prefix = '/post')

        @app.template_filter()
        def format_datetime(value):
            return value.strftime("%a %b %d, %Y at %I:%M:%S %p")

        import application.views

        return app

app = init_app()