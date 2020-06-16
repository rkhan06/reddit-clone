from flask import render_template, url_for, redirect
from flask_login import current_user, login_required

from app import db
from app.models.subreddit import Subreddit
from app.models.post import Post
from app.subreddit import subreddit
from .forms import CreateCommunityForm, PostForm


@login_required
@subreddit.route('/subreddit/create', methods=['GET', 'POST'])
def create():
    form = CreateCommunityForm()
    if form.validate_on_submit():
        new_sub = Subreddit(name=form.name.data,
                            description=form.description.data,
                            creator=current_user)
        db.session.add(new_sub)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('subreddit/create.html', form=form)


@login_required
@subreddit.route('/r/<name>', methods=['GET', 'POST'])
def subreddit(name):
    subreddit = Subreddit.query.filter_by(name=name).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(text=form.post_text.data, author=current_user,
                        subreddit=subreddit)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('subreddit.subreddit', name=name))
    posts = Post.query.filter_by(subreddit=subreddit)
    return render_template('subreddit/subreddit.html',
                           subreddit=subreddit,
                           form=form,
                           posts=posts)
