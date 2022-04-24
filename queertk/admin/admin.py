from flask import Blueprint, render_template

# Create Blueprint
bp_admin = Blueprint("bp_admin", __name__, static_folder = "static", template_folder = "templates")

from queertk import app
from database import db
from flask_admin import Admin
from queertk.models import *

# Initialize database and Admin
admin = Admin(app)
db.init_app(app)

from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin import BaseView, expose

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('customview.html')

class ArtistModelView(ModelView):
    # Options: https://readthedocs.org/projects/flask-admin/downloads/pdf/latest/
    # Replace the default ModelView (used below to render admin model pages)

    # Hide columns from list view
    column_exclude_list = ['biography']

    # Which columns can you search by
    column_searchable_list = ['artist_name', 'legal_name', 'short_name']

    # Which columns can you edit inline from list view
    column_editable_list = ['artist_name', 'birthday', 'slug']

    # Which column is list view sorted by by default
    column_default_sort = 'artist_name'

    # Table can be exported
    can_export = True
    can_view_details = True

    #Enable modals
    create_modal = True
    details_modal = True
    edit_modal = True

    # Question mark next to field name, hover to see description
    column_descriptions = dict(
        artist_name = 'Stage name, credit name, etc.'
    )

    # Determine which fields are visible to create and edit.
    form_rules = [
        rules.FieldSet(('artist_name', 'legal_name', 'short_name', 'birthday', 'biography', 'headshot', 'slug'), 'Artist')
    ]

    def get_save_return_url(self, model, is_created):
        return self.get_url('.details_view', id='model.id')

class PlayModelView(ModelView):
    column_searchable_list = ['title', 'author']
    page_size = 50

class PerformanceModelView(ModelView):
    column_filters = ['production_id']

class ProductionModelView(ModelView):
    # Question mark next to field name, hover to see description
    column_descriptions = dict(
        slug = 'This value is used to create the URL to the production, i.e. /prod/season-9/say-cheesecake'
    )

# Add views
admin.add_view(ArtistModelView(Artist, db.session, category = "People"))
admin.add_view(ModelView(Credit, db.session, category = "People"))
admin.add_view(ModelView(NoticeType, db.session, category = "Reference"))
admin.add_view(ModelView(Notice, db.session, category = "Production"))
admin.add_view(PerformanceModelView(Performance, db.session, category = "Production"))
admin.add_view(PlayModelView(Play, db.session, category = "Reference"))
admin.add_view(ModelView(ProductionNotice, db.session, category = "Production"))
admin.add_view(ProductionModelView(Production, db.session, category = "Production"))
admin.add_view(ModelView(Season, db.session, category = "Reference"))
admin.add_view(ModelView(Venue, db.session, category = "Reference"))
admin.add_view(CustomView(name='Custom', endpoint='custom'))