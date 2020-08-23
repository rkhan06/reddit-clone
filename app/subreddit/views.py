from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_required

from app import db
from app.subreddit import subreddit
from app.models.subreddit import Subreddit
from app.models.post import Post
from app.models.comment import Comment
from app.core.forms import PostForm

from .forms import CreateCommunityForm, EmptyForm, CommentForm


@subreddit.route('/subreddit/create', methods=['GET', 'POST'])
@login_required
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


@subreddit.route('/r/<name>', methods=['GET', 'POST'])
def home(name):
    subreddit = Subreddit.query.filter_by(name=name).first_or_404()
    form = PostForm()
    empty_form = EmptyForm()
    if form.validate_on_submit():
        new_post = Post(text=form.post_text.data, author=current_user,
                        subreddit=subreddit)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('subreddit.home', name=name))
    posts = Post.query.filter_by(subreddit=subreddit)
    return render_template('subreddit/home.html',
                           subreddit=subreddit,
                           form=form,
                           posts=posts, empty_form=empty_form)


@subreddit.route('/subscribe/<subreddit>', methods=['POST'])
@login_required
def subscribe(subreddit):
    sub = Subreddit.query.filter_by(name=subreddit).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        current_user.subscribe(sub)
        db.session.commit()
        return redirect(url_for('subreddit.home', name=subreddit))
    return redirect(url_for('core.index'))


@subreddit.route('/unsubscribe/<subreddit>', methods=['POST'])
@login_required
def unsubscribe(subreddit):
    sub = Subreddit.query.filter_by(name=subreddit).first_or_404()
    form = EmptyForm()
    if form.validate_on_submit():
        current_user.unsubscribe(sub)
        db.session.commit()
        return redirect(url_for('core.index', name=subreddit))
    return redirect(url_for('core.index'))


@subreddit.route('/r/<subreddit>/post/<int:id>', methods=['GET', 'POST'])
def post(subreddit, id):
    sub = Subreddit.query.filter_by(name=subreddit).first_or_404()
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            if form.validate_on_submit():
                if int(request.form['parent']) > 0:
                    new_comment = Comment(
                        post=post, text=form.comment.data,
                        author=current_user,
                        parent_id=int(request.form['parent']))
                else:
                    new_comment = Comment(post=post, text=form.comment.data,
                                          author=current_user)
                db.session.add(new_comment)
                db.session.commit()
                return redirect(url_for('subreddit.post',
                                        subreddit=sub.name, id=id))
        else:
            return redirect(url_for('auth.login'))
    else:
        return render_template('subreddit/post.html', subreddit=sub,
                               post=post, comment_form=form)
