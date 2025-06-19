from flask import  render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify, current_app
from flask_login import login_required, current_user
from gingerblog import db
from gingerblog.models import Post, Like
from gingerblog.posts.forms import PostForm, EmptyForm
from werkzeug.utils import secure_filename
from gingerblog.posts.utils import save_post_image
from gingerblog.utils.summarizer import summarize_text
from gingerblog import cache
from time import time
import os




posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = save_post_image(form.image.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, image_file=image_file)
        db.session.add(post)
        db.session.commit()
        flash('Your post sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EmptyForm()
    return render_template('post.html', title = post.title, post = post, form=form)



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', form = form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EmptyForm()
    
    if form.validate_on_submit():
        if post.author != current_user:
            abort(403)

        # Remove the post image if it's not the default
        if post.image_file and post.image_file != 'default.jpg':
            image_path = os.path.join(current_app.root_path, 'static/post_images', post.image_file)
            if os.path.exists(image_path):
                os.remove(image_path)

        for like in post.likers.all():  
            db.session.delete(like)  

        db.session.commit() 

        db.session.delete(post)
        db.session.commit()

        flash('Your post has been deleted!', 'success')
        return redirect(url_for('main.home'))

    abort(400)


@posts.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    total_start = time()

    # Check if the user already liked the post
    t1 = time()
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    t2 = time()
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        db.session.add(Like(user_id=current_user.id, post_id=post_id))
        liked = True
    print(f"DB Add/Delete like time: {time() - t2:.4f}s")

    t3 = time()
    db.session.commit()

    t4 = time()
    like_count = cache.get(f"like_count_{post_id}")
    if like_count is None:
        print(" Cache miss: Fetching fresh count from DB")
        like_count = Like.query.filter_by(post_id=post_id).count()
    else:
        print(" Cache hit")
        like_count = like_count + 1 if liked else like_count - 1

    cache.set(f"like_count_{post_id}", like_count, timeout=300)

    print(f"Total like route time: {time() - total_start:.4f}s")

    return jsonify({'likes': like_count, 'liked': liked})



@posts.route("/api/summarize/<int:post_id>")
@login_required
def api_summarize_post(post_id):
    post = Post.query.get_or_404(post_id)
    summarized_content = summarize_text(post.content)
    return jsonify({'summary': summarized_content})
