from .admin import admin

# Import custom ModelViews
from queertk.blueprints.admin.models import *

# Import all models that need admin view
from queertk.blueprints.post.models import Post
from queertk.blueprints.artist.models import Artist
from queertk.blueprints.production.models import Production, ProductionNotice, Performance
from queertk.blueprints.common.models import *

# Import database object
from queertk.database import db

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
admin.add_view(ModelView(Post, db.session, category = "News"))

# Add a blank page (view) to the admin menu
admin.add_view(CustomView(name='Custom', endpoint='custom'))