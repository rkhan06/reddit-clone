from flask import render_template, request, redirect, url_for, jsonify
from flask_login import current_user

from app import db
from app.models.user import User
from app.models.subreddit import Subreddit
from app.models.post import Post
from flask_login import login_required
from app.core import core
from app.core.forms import PostForm
from app.subreddit.forms import EmptyForm


@core.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    posts = Post.query.all()
    subreddits = Subreddit.query.all()
    empty_form = EmptyForm()
    return render_template('core/index.html', users=users,
                           subreddits=subreddits, posts=posts,
                           empty_form=empty_form)


@core.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    default_choice = [(0, 'Choose Community')]
    form.community.choices = default_choice + [
        (sub.id, "r/"+sub.name) for sub in Subreddit.query.all()]

    if request.method == 'POST':
        if form.validate_on_submit():
            community = Subreddit.query.filter_by(
                id=form.community.data).first()
            new_post = Post(title=form.title.data,
                            description=form.description.data,
                            subreddit=community,
                            author=current_user)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('core.index'))

    return render_template('core/create_post.html', form=form)


@core.route('/upvote', methods=['POST'])
@login_required
def upvote():
    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    response = dict()
    if post is not None:
        res = post.upvote(current_user)
        db.session.commit()
        response['message'] = 'success'
        response['value'] = res
        response['votes'] = post.votes()
        return jsonify(response), 200

    response['message'] = 'error'

    return jsonify(response), 200


@core.route('/downvote', methods=['POST'])
@login_required
def downvote():
    data = request.get_json()
    post = Post.query.filter_by(id=data['post_id']).first()
    response = dict()
    if post is not None:
        res = post.downvote(current_user)
        db.session.commit()
        response['message'] = 'success'
        response['value'] = res
        response['votes'] = post.votes()
        return jsonify(response), 200

    response['message'] = 'error'

    return jsonify(response), 200
