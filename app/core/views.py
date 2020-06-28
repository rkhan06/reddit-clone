from flask import render_template, request, redirect, url_for
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


@core.route('/upvote/<int:id>', methods=['POST'])
@login_required
def upvote(id):
    post = Post.query.filter_by(id=id).first()
    form = EmptyForm()

    if form.validate_on_submit() and post is not None:
        post.upvote(current_user)
        db.session.commit()
        return redirect(url_for('core.index'))

    return redirect(url_for('core.index'))


@core.route('/downvote/<int:id>', methods=['POST'])
@login_required
def downvote(id):
    post = Post.query.filter_by(id=id).first()
    form = EmptyForm()

    if form.validate_on_submit() and post is not None:
        post.downvote(current_user)
        db.session.commit()
        return redirect(url_for('core.index'))

    return redirect(url_for('core.index'))
