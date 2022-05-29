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
        from application.blueprints.person import bp_person
        from application.blueprints.post import bp_post

        app.register_blueprint(bp_common)
        # app.register_blueprint(bp_admin, url_prefix = '/admin')
        app.register_blueprint(bp_management, url_prefix = '/app')
        app.register_blueprint(bp_production, url_prefix = '/production')
        app.register_blueprint(bp_person, url_prefix = '/person')
        app.register_blueprint(bp_post)

        # Dec 11, 2021 at 07:30:00 PM
        @app.template_filter()
        def format_datetime(value):
            return value.strftime("%b %d, %Y at %I:%M:%S %p")

        # Dec 11
        @app.template_filter()
        def format_date_short(value):
            return value.strftime("%b %d")

        # 2022
        @app.template_filter()
        def format_date_year(value):
            return value.strftime("%Y")

        # Month N, 2022
        @app.template_filter()
        def format_post_date(value):
            return value.strftime("%b %d, %Y at %-I:%M %p")

        import application.views

        return app

app = init_app()