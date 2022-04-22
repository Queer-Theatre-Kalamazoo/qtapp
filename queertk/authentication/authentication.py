from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from .forms import RegisterForm
from .models import db, User

# Create blueprint
bp_authentication = Blueprint("authentication", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/auth") # Create Blueprint

# Create LoginManager
login_manager = LoginManager()

from queertk import app

# Instatiate Flask-Admin app
login_manager.init_app(app)
from . import login_manager

@bp_authentication.route('/login', methods=['GET', 'POST'])
def login():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                website=form.website.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template(
        'login.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


@bp_authentication.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # User sign-up logic will go here.
        ...
    return render_template(
        'register.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )