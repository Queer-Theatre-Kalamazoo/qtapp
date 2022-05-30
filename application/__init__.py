from flask import Flask
from flask_mail import Mail
from sqlalchemy import create_engine
from flask_ckeditor import CKEditor

def init_app():
    # Initialize the core application
    app = Flask(__name__, instance_relative_config=True)

    # Select and load config object dynamically based on the value of FLASK_ENV in .env
    if app.config["ENV"] == "production":
        app.config.from_object("application.config.ProductionConfig")
    else:
        app.config.from_object("application.config.DevelopmentConfig")

    # Globally accessible libraries?
    ckeditor = CKEditor()
    mail = Mail()


    with app.app_context():
        from application.blueprints.common import bp_common
        from application.blueprints.management import bp_management
        from application.blueprints.production import bp_production
        from application.blueprints.person import bp_person
        from application.blueprints.post import bp_post

        app.register_blueprint(bp_common)
        app.register_blueprint(bp_management, url_prefix = '/app')
        app.register_blueprint(bp_production, url_prefix = '/production')
        app.register_blueprint(bp_person)
        app.register_blueprint(bp_post)

        ckeditor.init_app(app)
        mail.init_app(app)
        app.mail = mail

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

# Remove or comment the line below when running via WSGI
app = init_app()