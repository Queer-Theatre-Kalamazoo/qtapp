from .admin import admin

# Import custom ModelViews
from queertk.blueprints.admin.models import *

# Import all models that need admin view
from queertk.blueprints.post.models import Post
from queertk.blueprints.artist.models import Artist
from queertk.blueprints.production.models import Production, ProductionNotice, Performance
from queertk.blueprints.common.models import *

# Import database object
from queertk.database import Session

# Add views
with Session.begin() as session:
    admin.add_view(ArtistModelView(Artist, session, category = "People"))
    admin.add_view(ModelView(Credit, session, category = "People"))
    admin.add_view(ModelView(NoticeType, session, category = "Reference"))
    admin.add_view(ModelView(Notice, session, category = "Production"))
    admin.add_view(PerformanceModelView(Performance, session, category = "Production"))
    admin.add_view(PlayModelView(Play, session, category = "Reference"))
    admin.add_view(ModelView(ProductionNotice, session, category = "Production"))
    admin.add_view(ProductionModelView(Production, session, category = "Production"))
    admin.add_view(ModelView(Season, session, category = "Reference"))
    admin.add_view(ModelView(Venue, session, category = "Reference"))
    admin.add_view(ModelView(Post, session, category = "News"))

    # Add a blank page (view) to the admin menu
    admin.add_view(CustomView(name='Custom', endpoint='custom'))