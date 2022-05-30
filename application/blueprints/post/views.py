from flask import render_template, url_for, request, redirect

# Import remote models
from application.blueprints.common.schema import Artist, Post, Person

# Import local models
from . import bp_post

# Import database object
from application.database import Session
from sqlalchemy import select, and_

# Get variable values for display_person() breadcrumbs
def bc_view_post(*args, **kwargs):
    with Session.begin() as session:
        post_id = request.view_args['post_id']
        post_query = select(Post.post_id, Post.category, Post.title).where(Post.post_id == post_id)
        post = session.execute(post_query).one()
        return [{'text': post.title, 'url': Post.get_url(post)}]


@bp_post.route("/<string:category>/<int:post_id>")
def display_post(category, post_id):
    category = category.lower()
    with Session.begin() as session:
        post = session.execute(select(Post.post_id, Post.category, Post.title, Post.subtitle, Post.content, Post.person_id).where(Post.post_id == post_id)).one()
        author = (
            session.execute(select(Person).where(Person.person_id == post.person_id)).scalars().one()
        )
        return render_template("post.html", post=post, author=author, title=post.title)

@bp_post.route("/news")
def index_news():
    with Session.begin() as session:
        posts = session.execute(
            select(
                Post.title, 
                Post.subtitle, 
                Post.content, 
                Post.snippet, 
                Post.post_id, 
                Post.category, 
                Post.create_date, 
                Person.name, 
                Person.person_id
            ).where(Post.category == "news").join(Person, Post.person_id == Person.person_id).order_by(Post.create_date.desc())
            ).all()
        return render_template('index_news.html', title='News', posts=posts)