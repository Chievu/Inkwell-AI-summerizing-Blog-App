from flask import render_template, Blueprint, request
from gingerblog.models import Post

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts= posts)
   

@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/search")
def search():
    query = request.args.get('query')
    if query:
        posts = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    else:
        posts = []
    return render_template('search_results.html', posts=posts, query=query)