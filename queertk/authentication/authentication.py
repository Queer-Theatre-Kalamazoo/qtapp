from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from .forms import RegisterForm, LoginForm
from .models import db, User
from datetime import datetime

# Create blueprint
bp_authentication = Blueprint("authentication", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/auth") # Create Blueprint

# Create LoginManager
login_manager = LoginManager()

from queertk import app

# Instatiate Flask-Admin app
login_manager.init_app(app)

@bp_authentication.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    date = datetime.now()
    if form.validate_on_submit():
        # Used in next step to validate email and username are unique
        existing_email = User.query.filter_by(email=form.email.data).first()
        existing_username = User.query.filter_by(username=form.username.data).first()

        if existing_email is None and existing_username is None:
            # Create user object with form data since email and username ARE unique
            user = User(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                create_date=date
            )
            # The set_password method hashes the password
            user.set_password(form.password.data)

            # Add and commit user object to db
            db.session.add(user)
            db.session.commit()

            login_user(user)  # Log in as newly created user

            return redirect(url_for('views.home'))
        flash('A user already exists with that email address or username.')
    return render_template(
        'register.html',
        title='Create an Account.',
        form=form,
        template='register-page',
        body="Sign up for a user account."
    )


@bp_authentication.route('/login', methods=['GET', 'POST'])
def login():
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    # Validate login attempt
    if form.validate_on_submit():

        # Used in the next step to check password
        user = User.query.filter_by(email=form.email.data).first()

        # If user exists and password from form matches hash, log in
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Invalid username or password.')
        return redirect(url_for('authentication.login'))
    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )

@bp_authentication.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    # Check if user is logged-in on every page load
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to Login page
    flash('You must be logged in to view that page.')
    return redirect(url_for('authentication.login'))